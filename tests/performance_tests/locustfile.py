from locust import HttpUser, task, between


class PerfMonitoring(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_root(self):
        self.client.get("/")

    @task
    def load_summary_post(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def load_email_ko(self):
        self.client.post("/showSummary", data={"email": "notavalidemail"})

    @task
    def load_booking_url(self):
        self.client.get(
            "/book/competition_name/club_name",
            data={"club": "Simply Lift", "competition": "Spring Festival"},
        )

    @task
    def load_purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            data={"club": "Simply Lift", "competition": "Fall Classic", "places": 1},
        )

    @task
    def load_clubs_board(self):
        self.client.get("/clubs_board")

    @task
    def perform_logout(self):
        self.client.get("/logout")
