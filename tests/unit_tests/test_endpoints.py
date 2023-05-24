import json
import pytest
from flask import get_flashed_messages
import server


class TestEndpoints:
    """Testing the response status code of every endpoint, considering a few edge cases."""

    @pytest.fixture(autouse=True)
    def setup_clubs(self, mocker, data_fixture):
        mocker.patch("server.load_clubs", return_value=data_fixture["clubs"])
        mocker.patch(
            "server.load_competitions", return_value=data_fixture["competitions"]
        )
        self.clubs = server.load_clubs()
        self.competitions = server.load_competitions()

    def test_status_code_root(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_status_code_summary_post(self, client):
        email = self.clubs[0]["email"]
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 200

    def test_status_code_summary_get_email_ok(self, client):
        email = self.clubs[0]["email"]
        response = client.get(f"/show_summary_get/{email}", data={"email": email})
        assert response.status_code == 200

    def test_status_code_summary_get_email_ko(self, client):
        email = "test@test.fr"
        response = client.get(f"/show_summary_get/{email}", data={"email": email})
        assert response.status_code == 302
        assert get_flashed_messages() == ["Sorry, that email wasn't found"]

    def test_email_ko(self, client):
        email = "notavalidemail"
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 302

    def test_email_notfound(self, client):
        email = "test@test.fr"
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 302
        assert get_flashed_messages() == ["Sorry, that email wasn't found"]

    def test_booking_url(self, client):
        club = self.clubs[0]["name"]
        competition = self.competitions[1]["name"]

        response = client.get(
            f"/book/{competition}/{club}",
            data={"club": club, "competition": competition},
        )
        assert response.status_code == 200

    def test_clubs_board(self, client):
        response = client.get(
            "/clubs_board",
            data={"clubs": self.clubs, "competitions": self.competitions},
        )
        assert response.status_code == 200

    def test_logout(self, client):
        email = self.clubs[0]["email"]
        response = client.post("/showSummary", data={"email": email})
        assert response.status_code == 200
        response = client.get("/logout")
        assert response.status_code == 302
