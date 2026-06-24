#!/usr/bin/python3
import os
import sys

import requests
from requests.exceptions import HTTPError

if __name__ == "__main__":
    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1, PATH)
from logger import logger


class SendRequest:
    def get_request(self, url, params=None):
        try:
            response = requests.get(url, params=params)
        except HTTPError as http_err:
            logger.logger.error("%s - HTTP error : %s", __name__, http_err)
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.logger.error("%s - error : %s", __name__, err)
            print(f"Other error occurred: {err}")
        else:
            result = 0
            if response.status_code == 200:
                try:
                    result = response.json()
                except Exception as e:
                    print(e)
                finally:
                    return result
            else:
                return result

    def get_rainfall_data(self):
        data = {}
        result = self.get_request(
            "https://api-open.data.gov.sg/v2/real-time/api/rainfall"
        )
        if len(result) == 0:
            return data
        for item in result["data"]["stations"]:
            data[item["deviceId"]] = {}
            data[item["deviceId"]]["name"] = item["name"]
            data[item["deviceId"]]["location"] = item["location"]
        for item in result["data"]["readings"][0]["data"]:
            data[item["stationId"]]["timestamp"] = result["data"]["readings"][0][
                "timestamp"
            ]
            data[item["stationId"]]["value"] = item["value"]
        return data

    def get_air_temperature_data(self):
        data = {}
        result = self.get_request(
            "https://api-open.data.gov.sg/v2/real-time/api/air-temperature"
        )
        if len(result) == 0:
            return data
        for item in result["data"]["stations"]:
            data[item["id"]] = {}
            data[item["id"]]["name"] = item["name"]
            data[item["id"]]["location"] = item["location"]
        for item in result["data"]["readings"][0]["data"]:
            data[item["stationId"]]["timestamp"] = result["data"]["readings"][0][
                "timestamp"
            ]
            data[item["stationId"]]["temperature"] = item["value"]
        return data

    def get_two_hour_forecast(self):
        data = {}
        result = self.get_request(
            "https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast"
        )
        if len(result) == 0:
            return data
        for item in result["data"]["area_metadata"]:
            data[item["name"]] = {}
            data[item["name"]]["location"] = item["label_location"]

        for item in result["data"]["items"][0]["forecasts"]:
            data[item["area"]]["timestamp"] = result["data"]["items"][0]["timestamp"]
            data[item["area"]]["forecast"] = item["forecast"]
        return data


if __name__ == "__main__":
    t = SendRequest()

    r1 = t.get_rainfall_data()
    r2 = t.get_two_hour_forecast()
    r3 = t.get_air_temperature_data()
    for k in r1:
        for k1 in r2:
            if k1 in r1[k]["location"]:
                r1[k]["forecast"] = r2[k1]["forecast"]
                break

    print(r3)
