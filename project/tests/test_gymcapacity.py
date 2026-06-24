import json
from types import SimpleNamespace

from controller import gymcapacity
from controller.gymcapacity import GymCapacity
from error.error import DatabaseError, ErrorCode


class FakeScraper:
    def __init__(self, payload):
        self.payload = payload

    def get_data(self):
        return self.payload


class ExistingCoordinateDatabase:
    def query_one(self, table, **kwargs):
        return [{"id": 1, "area": kwargs["area"], "latitude": 1.3, "longitude": 103.8}]


class MissingCoordinateDatabase:
    def __init__(self):
        self.inserted = []
        self.coordinates = []

    def query_one(self, table, **kwargs):
        if not self.coordinates:
            raise DatabaseError("Not Found!", ErrorCode.NOT_FOUND.value)
        return self.coordinates

    def insert(self, table, values):
        self.inserted.append(values)
        self.coordinates = [{"id": 2, **values}]
        return 2


def test_get_data_uses_existing_coordinate():
    payload = {
        "timestamp": "2026-06-24 12:00:00",
        "data": {1: {"area": "Bishan", "name": "Bishan Gym", "capacity": "20%"}},
    }
    capacity = GymCapacity(database_model=ExistingCoordinateDatabase())
    capacity.scraper = FakeScraper(payload)

    result = capacity.get_data()

    assert result["data"][1]["coordinate"] == {
        "id": 1,
        "area": "Bishan",
        "latitude": 1.3,
        "longitude": 103.8,
    }


def test_get_data_geocodes_and_inserts_missing_coordinate():
    payload = {
        "timestamp": "2026-06-24 12:00:00",
        "data": {1: {"area": "Bishan", "name": "Bishan Gym", "capacity": "20%"}},
    }
    database = MissingCoordinateDatabase()
    capacity = GymCapacity(database_model=database)
    capacity.scraper = FakeScraper(payload)
    capacity.geocode = lambda address: SimpleNamespace(latitude=1.35, longitude=103.85)

    result = capacity.get_data()

    assert database.inserted[0]["area"] == "Bishan"
    assert result["data"][1]["coordinate"]["id"] == 2


def test_get_info_parses_sportsg_geojson(tmp_path, monkeypatch):
    assets_dir = tmp_path / "assets"
    assets_dir.mkdir()
    geojson_file = assets_dir / "SportSGSportFacilitiesGEOJSON.geojson"
    geojson_file.write_text(
        json.dumps(
            {
                "features": [
                    {
                        "properties": {
                            "Name": "Test Facility",
                            "Description": (
                                "<table><tr><th>skip</th><th>Gym</th>"
                                "<th>Road_Name</th></tr>"
                                "<tr><td>yes</td><td>Main Road</td></tr></table>"
                            ),
                        },
                        "geometry": {"coordinates": [[[[103.8, 1.3]]]]},
                    }
                ]
            }
        )
    )
    monkeypatch.setattr(gymcapacity, "PATH", str(tmp_path))

    result = GymCapacity(database_model=ExistingCoordinateDatabase()).get_info()

    assert result["Test Facility"]["geometry"] == [[103.8, 1.3]]
    assert result["Test Facility"]["gym"] == "yes"
    assert result["Test Facility"]["road_name"] == "main road"


def test_get_address_reads_cached_file(tmp_path):
    address_file = tmp_path / "gyms.txt"
    address_file.write_text("Cached Gym Address\n")

    result = GymCapacity(database_model=ExistingCoordinateDatabase()).get_address(
        file_path=str(tmp_path),
        file_name="gyms",
    )

    assert result == ["Cached Gym Address"]
