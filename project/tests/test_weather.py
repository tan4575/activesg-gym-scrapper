import pytest
from controller.weather import Weather


class FakeWeatherRequest:
    def get_rainfall_data(self):
        return {
            "RAIN-1": {
                "name": "Rain Station",
                "location": {"latitude": 1.300, "longitude": 103.800},
                "timestamp": "2026-06-24T12:00:00+08:00",
                "value": 3,
            }
        }

    def get_two_hour_forecast(self):
        return {
            "Far Area": {
                "location": {"latitude": 1.450, "longitude": 103.950},
                "forecast": "Fair",
            },
            "Near Area": {
                "location": {"latitude": 1.301, "longitude": 103.801},
                "forecast": "Thundery Showers",
            },
        }

    def get_air_temperature_data(self):
        return {
            "TEMP-FAR": {
                "location": {"latitude": 1.500, "longitude": 104.000},
                "temperature": 31.2,
            },
            "TEMP-NEAR": {
                "location": {"latitude": 1.302, "longitude": 103.802},
                "temperature": 28.6,
            },
        }


def test_haversine_returns_zero_for_same_coordinates():
    assert Weather.haversine(1.3, 103.8, 1.3, 103.8) == pytest.approx(0)


def test_haversine_calculates_distance_between_coordinates():
    result = Weather.haversine(1.300, 103.800, 1.301, 103.801)

    assert result == pytest.approx(0.157, abs=0.01)


def test_get_data_matches_nearest_forecast_and_temperature():
    weather = Weather()
    weather.request = FakeWeatherRequest()

    result = weather.get_data()

    assert result == [
        {
            "deviceId": "RAIN-1",
            "area": "Rain Station",
            "rainfall": 3,
            "forecast": "Thundery Showers",
            "time": "2026-06-24T12:00:00+08:00",
            "temperature": 28.6,
            "longitude": 103.800,
            "latitude": 1.300,
        }
    ]


def test_get_data_returns_empty_list_when_any_source_is_empty():
    class EmptyForecastRequest(FakeWeatherRequest):
        def get_two_hour_forecast(self):
            return {}

    weather = Weather()
    weather.request = EmptyForecastRequest()

    assert weather.get_data() == []
