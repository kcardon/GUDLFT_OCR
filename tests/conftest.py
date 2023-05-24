import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def data_fixture():
    data = {
        "clubs": [
            {
                "name": "Test_fewpoints",
                "email": "fewpoints@test.fr",
                "points": "1",
            },
            {
                "name": "test_manypoints",
                "email": "manypoints@test.fr",
                "points": "15",
            },
        ],
        "competitions": [
            {
                "name": "past_compet",
                "date": "2020-10-22 13:30:00",
                "numberOfPlaces": "10",
            },
            {
                "name": "future_compet",
                "date": "2024-10-22 13:30:00",
                "numberOfPlaces": "10",
            },
        ],
    }
    return data
