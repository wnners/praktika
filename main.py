from flask import Flask, request, jsonify
import time

app = Flask(__name__)


USERS = {
    "user@test.com": "Test1234!"
}

EVENTS = {
    1: {"title": "Концерт Imagine Dragons", "date": "2026-07-10", "category": "concert", "seats": 50},
    2: {"title": "Спектакль Гамлет", "date": "2026-07-15", "category": "theater", "seats": 30},
    3: {"title": "Кино: Интерстеллар", "date": "2026-07-20", "category": "cinema", "seats": 100},
    4: {"title": "Джазовый вечер", "date": "2026-07-22", "category": "concert", "seats": 40},
    5: {"title": "Балет Лебединое озеро", "date": "2026-07-25", "category": "theater", "seats": 60},
}

SESSIONS = {}   
BOOKINGS = {}   
booking_counter = [1000]

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    email    = data.get("email", "")
    password = data.get("password", "")

    if email not in USERS or USERS[email] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = f"jwt_{email.split('@')[0]}_{int(time.time())}"
    SESSIONS[token] = email
    return jsonify({
        "session_token": token,
        "user": email,
        "message": "Login successful"
    }), 200


@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json()
    email    = data.get("email", "")
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    if email in USERS:
        return jsonify({"error": "User already exists"}), 409

    USERS[email] = password
    return jsonify({"message": "Registered successfully", "user": email}), 201

@app.route("/api/catalog/events", methods=["GET"])
def get_events():
    category = request.args.get("category")
    date     = request.args.get("date")

    result = dict(EVENTS)

    if category:
        result = {k: v for k, v in result.items() if v["category"] == category}
    if date:
        result = {k: v for k, v in result.items() if v["date"] == date}

    events_list = [{"event_id": k, **v} for k, v in result.items()]
    return jsonify({"events": events_list, "count": len(events_list)}), 200


@app.route("/api/catalog/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    if event_id not in EVENTS:
        return jsonify({"error": "Event not found", "event_id": event_id}), 404
    return jsonify({"event_id": event_id, **EVENTS[event_id]}), 200



def get_user_from_token(req):
    auth = req.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.split(" ", 1)[1]
    return SESSIONS.get(token)


@app.route("/api/booking/create", methods=["POST"])
def create_booking():
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Invalid or expired session token", "code": "AUTH_FAILED"}), 401

    data     = request.get_json()
    event_id = data.get("event_id")

    if event_id not in EVENTS:
        return jsonify({"error": "Event not found", "event_id": event_id, "code": "EVENT_NOT_FOUND"}), 404

    booking_counter[0] += 1
    bid = booking_counter[0]
    BOOKINGS[bid] = {
        "booking_id": bid,
        "event_id":   event_id,
        "user":       user,
        "status":     "pending"
    }
    return jsonify(BOOKINGS[bid]), 200


@app.route("/api/booking/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Unauthorized", "code": "AUTH_FAILED"}), 401

    if booking_id not in BOOKINGS:
        return jsonify({"error": "Booking not found", "booking_id": booking_id}), 404

    return jsonify(BOOKINGS[booking_id]), 200


@app.route("/api/booking/cancel/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    if booking_id not in BOOKINGS:
        return jsonify({"error": "Booking not found"}), 404

    b = BOOKINGS[booking_id]
    if b["status"] == "paid":
        return jsonify({"error": "Cannot cancel paid booking"}), 409

    b["status"] = "cancelled"
    return jsonify({"message": "Booking cancelled", "booking_id": booking_id}), 200


@app.route("/api/booking/list", methods=["GET"])
def list_bookings():
    user = get_user_from_token(request)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    user_bookings = [b for b in BOOKINGS.values() if b["user"] == user]
    return jsonify({"bookings": user_bookings, "count": len(user_bookings)}), 200

@app.route("/api/payment/pay", methods=["POST"])
def pay():
    data       = request.get_json()
    booking_id = data.get("booking_id")
    card_token = data.get("card_token", "")

    if booking_id not in BOOKINGS:
        return jsonify({"error": "Booking not found", "booking_id": booking_id}), 404

    b = BOOKINGS[booking_id]

    if b["status"] == "paid":
        return jsonify({
            "error": "Booking already paid",
            "booking_id": booking_id,
            "current_status": "paid"
        }), 409

    if b["status"] == "cancelled":
        return jsonify({"error": "Booking is cancelled"}), 409


    if card_token == "tok_test_decline":
        BOOKINGS[booking_id]["status"] = "failed"
        return jsonify({
            "payment_status": "declined",
            "reason": "Insufficient funds",
            "booking_id": booking_id
        }), 402

    BOOKINGS[booking_id]["status"] = "paid"
    return jsonify({
        "payment_status": "success",
        "booking_id": booking_id,
        "message": "Payment accepted"
    }), 200


if __name__ == "__main__":
    print("=" * 50)
    print("  TicketBook API запущен!")
    print("  URL: http://127.0.0.1:5000")
    print("=" * 50)
    print()
    print("  Тестовый пользователь:")
    print("  Email:    user@test.com")
    print("  Password: Test1234!")
    print()
    print("  Эндпоинты:")
    print("  POST /api/auth/login")
    print("  POST /api/auth/register")
    print("  GET  /api/catalog/events")
    print("  GET  /api/catalog/events/<id>")
    print("  POST /api/booking/create")
    print("  GET  /api/booking/<id>")
    print("  POST /api/booking/cancel/<id>")
    print("  GET  /api/booking/list")
    print("  POST /api/payment/pay")
    print()
    print("  Для остановки: Ctrl+C")
    print("=" * 50)
    app.run(debug=False, port=5000)