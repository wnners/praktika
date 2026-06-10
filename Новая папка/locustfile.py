from locust import HttpUser, task, between

class DemoShopLoadUser(HttpUser):
    wait_time = between(1, 3)
    host = 'https://www.demoblaze.com'

    @task(3)
    def index_page(self):
        with self.client.get('/', catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Fail HTTP {resp.status_code}")

    @task(2)
    def filter_by_category(self):
        self.client.post('/bycat', json={'cat': 'phone'})

    @task(1)
    def view_product_details(self):
        self.client.post('/view', json={'id': '1'})

    @task(1)
    def inspect_cart(self):
        self.client.post('/viewcart', json={'cookie': 'guest', 'flag': True})