from flask import get_flashed_messages
import server
import pytest


class TestPurchase:
    """Covering different test cases for purchasing places including sad paths."""

    @pytest.fixture(autouse=True)
    def setup_clubs(self, mocker, data_fixture):
        mocker.patch("server.load_clubs", return_value=data_fixture["clubs"])
        mocker.patch(
            "server.load_competitions", return_value=data_fixture["competitions"]
        )
        self.clubs = server.load_clubs()
        self.competitions = server.load_competitions()

    def test_purchase_successful(self, client):
        club = self.clubs[0]
        competition = next(c for c in self.competitions if c["name"] == "future_compet")
        places_required = 1
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": places_required,
            },
        )
        assert response.status_code == 200
        assert "You purchase is completed." in get_flashed_messages()

    def test_shouldnt_purchase_more_than_available_points(self, client):
        club = self.clubs[0]
        competition = next(c for c in self.competitions if c["name"] == "future_compet")
        places_required = int(club["points"]) + 1
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": places_required,
            },
        )

        assert response.status_code == 302
        with client.application.app_context():
            assert "You don't have enough points." in get_flashed_messages()

    def test_shouldnt_purchase_more_than_twelve(self, client):
        club = next(c for c in self.clubs if c["name"] == "test_manypoints")
        competition = next(c for c in self.competitions if c["name"] == "future_compet")
        places_required = 13
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": places_required,
            },
        )

        assert response.status_code == 302
        with client.application.app_context():
            assert "You can't book more than 12 places" in get_flashed_messages()

    def test_shouldnt_book_past_competition(self, client):
        club = self.clubs[0]
        competition = self.competitions[0]
        response = client.get(
            f"/book/{competition['name']}/{club['name']}",
            data={"club": club, "competition": competition},
        )
        assert response.status_code == 302
        with client.application.app_context():
            assert (
                "You can't book places on a past competition." in get_flashed_messages()
            )

    def test_purchase_updates_club_points(self, client):
        club = self.clubs[0]
        competition = self.competitions[1]
        club_points = club["points"]
        places_required = 1
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": places_required,
            },
        )
        assert response.status_code == 200
        assert int(self.clubs[0]["points"]) == int(club_points) - 1

    def test_purchase_updates_competition_available_places(self, client):
        club = self.clubs[0]
        competition = self.competitions[1]
        competition_places = competition["numberOfPlaces"]
        places_required = 1
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": places_required,
            },
        )
        assert response.status_code == 200
        assert (
            int(self.competitions[1]["numberOfPlaces"]) == int(competition_places) - 1
        )

    def test_shouldnt_purchase_more_than_available(self, client):
        club = self.clubs[1]
        competition = self.competitions[0]
        places_required = int(competition["numberOfPlaces"]) + 1
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club["name"],
                "competition": competition["name"],
                "places": places_required,
            },
        )
        assert response.status_code == 200
        with client.application.app_context():
            assert "The competition is full." in get_flashed_messages()
