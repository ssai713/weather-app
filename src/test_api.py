import pytest
from src.app import app, db, WeatherRecord

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture
def weather_record():
    def create_weather_record(
        station="station_name",
        date="19850106",
        maximum_temperature=10,
        minimum_temperature=8,
        precipitation=20,
    ):
        record = WeatherRecord(
            station=station,
            date=date,
            maximum_temperature=maximum_temperature,
            minimum_temperature=minimum_temperature,
            precipitation=precipitation,
        )
        db.session.add(record)
        db.session.commit()
        return record
    return create_weather_record

def test_get_weather_reports(client, weather_record):
    # create a weather record for testing
    weather_record()

    # test successful request
    response = client.get("/api/weather/")
    assert response.status_code == 200
    assert response.json == [
        {
            "date": "19850106",
            "maximum_temperature": 10,
            "minimum_temperature": 8,
            "precipitation": 20,
            "station": "station_name",
        }
    ]

    # test request with missing data
    db.session.query(WeatherRecord).delete()
    db.session.commit()
    response = client.get("/api/weather/abcd")
    assert response.status_code == 404
