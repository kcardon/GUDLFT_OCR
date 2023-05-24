from server import load_clubs, load_competitions


class TestServer:
    def test_load_clubs(self):
        clubs = load_clubs()
        club = clubs[0]
        assert isinstance(club["name"], str)
        assert isinstance(club["email"], str)
        assert isinstance(int(club["points"]), int)

    def test_load_competitions(self):
        competitions = load_competitions()
        competition = competitions[0]
        assert isinstance(competition["name"], str)
        assert isinstance(competition["date"], str)
        assert isinstance(int(competition["numberOfPlaces"]), int)
