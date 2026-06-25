import json
from types import SimpleNamespace
from unittest.mock import MagicMock

from controller import gymcapacity
from controller.gymcapacity import GymCapacity
from error.error import DatabaseError, ErrorCode


def build_existing_coordinate_database():
    database = MagicMock()
    database.query_one.return_value = [
        {"id": 1, "area": "Bishan", "latitude": 1.3, "longitude": 103.8}
    ]
    return database


def test_get_data_uses_existing_coordinate():
    payload = {
        "timestamp": "2026-06-24 12:00:00",
        "data": {1: {"area": "Bishan", "name": "Bishan Gym", "capacity": "20%"}},
    }
    database = build_existing_coordinate_database()
    capacity = GymCapacity(database_model=database)
    capacity.scraper = MagicMock()
    capacity.scraper.get_data.return_value = payload

    result = capacity.get_data()

    capacity.scraper.get_data.assert_called_once_with()
    database.query_one.assert_called_once()
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
    database = MagicMock()
    database.query_one.side_effect = [
        DatabaseError("Not Found!", ErrorCode.NOT_FOUND.value),
        [
            {
                "id": 2,
                "area": "Bishan",
                "latitude": 1.35,
                "longitude": 103.85,
                "time": "now",
            }
        ],
    ]
    capacity = GymCapacity(database_model=database)
    capacity.scraper = MagicMock()
    capacity.scraper.get_data.return_value = payload
    capacity.geocode = MagicMock(
        return_value=SimpleNamespace(latitude=1.35, longitude=103.85)
    )

    result = capacity.get_data()

    capacity.geocode.assert_called_once_with("Bishan Singapore")
    database.insert.assert_called_once()
    assert database.insert.call_args.args[1]["area"] == "Bishan"
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

    result = GymCapacity(database_model=build_existing_coordinate_database()).get_info()

    assert result["Test Facility"]["geometry"] == [[103.8, 1.3]]
    assert result["Test Facility"]["gym"] == "yes"
    assert result["Test Facility"]["road_name"] == "main road"


def test_get_address_reads_cached_file(tmp_path):
    address_file = tmp_path / "gyms.txt"
    address_file.write_text("Cached Gym Address\n")

    result = GymCapacity(
        database_model=build_existing_coordinate_database()
    ).get_address(
        file_path=str(tmp_path),
        file_name="gyms",
    )

    assert result == ["Cached Gym Address"]
