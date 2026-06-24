from unittest.mock import MagicMock

from httprequests.send_request import SendRequest


def test_get_request_returns_json_for_success(monkeypatch):
    class Response:
        status_code = 200

        @staticmethod
        def json():
            return {"ok": True}

    fake_get = MagicMock(return_value=Response())

    monkeypatch.setattr("httprequests.send_request.requests.get", fake_get)

    result = SendRequest().get_request("https://example.test", {"q": "gym"})

    assert result == {"ok": True}
    fake_get.assert_called_once_with("https://example.test", params={"q": "gym"})


def test_get_request_returns_zero_for_non_success_status(monkeypatch):
    class Response:
        status_code = 503

    fake_get = MagicMock(return_value=Response())
    monkeypatch.setattr("httprequests.send_request.requests.get", fake_get)

    assert SendRequest().get_request("https://example.test") == 0
    fake_get.assert_called_once_with("https://example.test", params=None)


def test_get_request_returns_zero_for_invalid_json(monkeypatch):
    class Response:
        status_code = 200

        @staticmethod
        def json():
            raise ValueError("not json")

    fake_get = MagicMock(return_value=Response())
    monkeypatch.setattr("httprequests.send_request.requests.get", fake_get)

    assert SendRequest().get_request("https://example.test") == 0
    fake_get.assert_called_once_with("https://example.test", params=None)


def test_get_rainfall_data_maps_stations_and_readings(monkeypatch):
    payload = {
        "data": {
            "stations": [
                {
                    "deviceId": "S1",
                    "name": "Station One",
                    "location": {"latitude": 1.3, "longitude": 103.8},
                }
            ],
            "readings": [
                {
                    "timestamp": "2026-06-24T12:00:00+08:00",
                    "data": [{"stationId": "S1", "value": 2}],
                }
            ],
        }
    }
    client = SendRequest()
    client.get_request = MagicMock(return_value=payload)

    result = client.get_rainfall_data()

    client.get_request.assert_called_once_with(
        "https://api-open.data.gov.sg/v2/real-time/api/rainfall"
    )
    assert result == {
        "S1": {
            "name": "Station One",
            "location": {"latitude": 1.3, "longitude": 103.8},
            "timestamp": "2026-06-24T12:00:00+08:00",
            "value": 2,
        }
    }


def test_get_two_hour_forecast_maps_area_metadata(monkeypatch):
    payload = {
        "data": {
            "area_metadata": [
                {
                    "name": "Ang Mo Kio",
                    "label_location": {"latitude": 1.37, "longitude": 103.85},
                }
            ],
            "items": [
                {
                    "timestamp": "2026-06-24T12:00:00+08:00",
                    "forecasts": [{"area": "Ang Mo Kio", "forecast": "Cloudy"}],
                }
            ],
        }
    }
    client = SendRequest()
    client.get_request = MagicMock(return_value=payload)

    result = client.get_two_hour_forecast()

    client.get_request.assert_called_once_with(
        "https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast"
    )
    assert result == {
        "Ang Mo Kio": {
            "location": {"latitude": 1.37, "longitude": 103.85},
            "timestamp": "2026-06-24T12:00:00+08:00",
            "forecast": "Cloudy",
        }
    }


def test_get_air_temperature_data_maps_station_temperatures(monkeypatch):
    payload = {
        "data": {
            "stations": [
                {
                    "id": "T1",
                    "name": "Temperature One",
                    "location": {"latitude": 1.31, "longitude": 103.81},
                }
            ],
            "readings": [
                {
                    "timestamp": "2026-06-24T12:00:00+08:00",
                    "data": [{"stationId": "T1", "value": 29.4}],
                }
            ],
        }
    }
    client = SendRequest()
    client.get_request = MagicMock(return_value=payload)

    result = client.get_air_temperature_data()

    client.get_request.assert_called_once_with(
        "https://api-open.data.gov.sg/v2/real-time/api/air-temperature"
    )
    assert result == {
        "T1": {
            "name": "Temperature One",
            "location": {"latitude": 1.31, "longitude": 103.81},
            "timestamp": "2026-06-24T12:00:00+08:00",
            "temperature": 29.4,
        }
    }
