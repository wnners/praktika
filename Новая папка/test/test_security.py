import pytest
import requests
import time

BASE_URL = 'https://www.demoblaze.com'

SQL_PAYLOADS = [
    ("' OR '1'='1", "Classic Injection"),
    ("' OR 1=1 --", "Comment Injection"),
    ("admin'--", "Password Bypass"),
    ("' UNION SELECT 1--", "Union Injection"),
    ("'; DROP TABLE users--", "Destructive Attempt")
]

WEAK_PASSWORDS = [
    ('123', 'Too Short'),
    ('password', 'Common Dictionary'),
    ('12345678', 'Digits Only'),
    ('aaaaaaaaa', 'Repeated Chars'),
    ('user@test', 'Username Match')
]

SECURITY_HEADERS = {
    'X-Frame-Options': 'Clickjacking Protection',
    'X-Content-Type-Options': 'MIME-Sniffing Protection',
    'Strict-Transport-Security': 'HSTS forcing HTTPS',
    'Content-Security-Policy': 'XSS Mitigation'
}

def test_sec_01_sql_injection_auth():
    print('\n=== SEC-01: SQL Injection Login Vulnerability Report ===')
    for payload, desc in SQL_PAYLOADS:
        payload_data = {"username": payload, "password": "wrong_password"}
        response = requests.post("https://api.demoblaze.com/login", json=payload_data, timeout=10)
        status = "VULNERABLE" if response.status_code == 200 and "token" in response.text else "SECURE"
        print(f"  Payload: {payload:25s} | Desc: {desc:30s} | Status: {status}")

def test_sec_02_weak_passwords_policy():
    print('\n=== SEC-02: Password Complexity Enforcement Check ===')
    for pwd, desc in WEAK_PASSWORDS:
        fake_username = f"qa_heavy_{int(time.time())}_{pwd[:2]}"
        payload_data = {"username": fake_username, "password": pwd}
        response = requests.post("https://api.demoblaze.com/signup", json=payload_data, timeout=10)
        accepted = "successful" in response.text.lower() or response.status_code == 200
        status = "VULNERABLE (Accepted)" if accepted else "OK (Rejected)"
        print(f"  Password: {pwd:15s} | Strength: {desc:20s} | System Response: {status}")

def test_sec_03_security_headers_compliance():
    response = requests.get(BASE_URL, timeout=10)
    print('\n=== SEC-03: Security Headers Compliance Matrix ===')
    missing_count = 0
    for header, desc in SECURITY_HEADERS.items():
        value = response.headers.get(header, None)
        status = f"[OK] {value}" if value else "[MISSING]"
        if not value:
            missing_count += 1
        print(f"  {header:30s}: {status} ({desc})")
    print(f"\nSummary: {missing_count} out of {len(SECURITY_HEADERS)} security headers are missing.")