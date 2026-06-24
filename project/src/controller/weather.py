#!/usr/bin/python3
import math
import os
import sys

if __name__ == "__main__":
    import os
    import sys

    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1, PATH)

from httprequests import send_request

EARTH_RADIUS_KM = 6371


class Weather:
    def __init__(self):
        self.request = send_request.SendRequest()

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        delta_latitude = (lat2 - lat1) * math.pi / 180.0
        delta_longitude = (lon2 - lon1) * math.pi / 180.0

        # convert to radians
        lat1 = lat1 * math.pi / 180.0
        lat2 = lat2 * math.pi / 180.0

        a = pow(math.sin(delta_latitude / 2), 2) + pow(
            math.sin(delta_longitude / 2), 2
        ) * math.cos(lat1) * math.cos(lat2)
        c = 2 * math.asin(math.sqrt(a))
        return EARTH_RADIUS_KM * c

    def get_data(self):
        rainfall_data = self.request.get_rainfall_data()
        forecast_data = self.request.get_two_hour_forecast()
        temperature_data = self.request.get_air_temperature_data()
        results = []
        if (
            len(rainfall_data) == 0
            or len(forecast_data) == 0
            or len(temperature_data) == 0
        ):
            return results
        for station_id in rainfall_data:
            rainfall_data[station_id]["area"] = None

            # weather forecast matching
            distance = float("inf")
            for forecast_area in forecast_data:
                coord_dist = self.haversine(
                    forecast_data[forecast_area]["location"]["latitude"],
                    forecast_data[forecast_area]["location"]["longitude"],
                    rainfall_data[station_id]["location"]["latitude"],
                    rainfall_data[station_id]["location"]["longitude"],
                )
                if coord_dist < distance:
                    distance = coord_dist
                    rainfall_data[station_id]["forecast"] = forecast_data[
                        forecast_area
                    ]["forecast"]
                    rainfall_data[station_id]["area"] = forecast_area
            # temperature
            distance = float("inf")
            for temperature_station_id in temperature_data:
                coord_dist = self.haversine(
                    temperature_data[temperature_station_id]["location"]["latitude"],
                    temperature_data[temperature_station_id]["location"]["longitude"],
                    rainfall_data[station_id]["location"]["latitude"],
                    rainfall_data[station_id]["location"]["longitude"],
                )
                if coord_dist < distance:
                    distance = coord_dist
                    rainfall_data[station_id]["temperature"] = temperature_data[
                        temperature_station_id
                    ]["temperature"]

        for station_id in rainfall_data:
            data = {}
            data["deviceId"] = station_id
            if rainfall_data[station_id].get("name") is not None:
                data["area"] = rainfall_data[station_id]["name"]
            if rainfall_data[station_id].get("value") is not None:
                data["rainfall"] = rainfall_data[station_id]["value"]
            if rainfall_data[station_id].get("forecast") is not None:
                data["forecast"] = rainfall_data[station_id]["forecast"]
            data["time"] = rainfall_data[station_id]["timestamp"]
            if rainfall_data[station_id].get("temperature") is not None:
                data["temperature"] = rainfall_data[station_id]["temperature"]
            data["longitude"] = rainfall_data[station_id]["location"]["longitude"]
            data["latitude"] = rainfall_data[station_id]["location"]["latitude"]
            results.append(data)
        return results


if __name__ == "__main__":
    from database import table
    from model import model

    a = Weather()
    for data in a.get_data():
        print(data)
    #     model.model.insert(table.weather, data)
    model.model.query_all(table.weather, True)
