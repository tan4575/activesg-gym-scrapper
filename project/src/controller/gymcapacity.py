#!/usr/bin/python3
import os
import sys

PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])

if __name__ == "__main__":
    sys.path.insert(1, PATH)

import datetime
import json
import random
import string
import time

from bs4 import BeautifulSoup
from database import table
from error import error
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim
from logger import logger
from web import scrapping


class GymCapacity:
    def __init__(self, database_model=None):
        self.scraper = scrapping.Scraper("https://activesg.gov.sg/gym-capacity")
        self.name = self.id_generator()
        self.geo_locator = Nominatim(user_agent=self.name)
        if database_model is None:
            from model.model import model as database_model

        self.database_model = database_model

    def id_generator(self, size=10):
        return "".join(
            random.SystemRandom().choice(string.ascii_uppercase + string.digits)
            for _ in range(size)
        )

    def geocode(self, address, attempt=1, max_attempts=5):
        try:
            return self.geo_locator.geocode(address)
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            logger.logger.info(
                "%s - timeout attempt : %d error : %s", __name__, attempt, e
            )
            if attempt <= max_attempts:
                self.name = self.id_generator()
                self.geo_locator = Nominatim(user_agent=self.name)
                time.sleep(0.05)
                return self.geocode(address, attempt=attempt + 1)
            raise

    def get_data(self):
        data = self.scraper.get_data()
        if len(data) == 0:
            return data
        for key in data["data"]:
            try:
                data["data"][key]["coordinate"] = self.database_model.query_one(
                    table.coordinate, area=data["data"][key]["area"]
                )[0]
            except Exception as e:
                err = str(e).split("Error Code:")
                if err[-1].strip() == str(error.ErrorCode.NOT_FOUND.value):
                    location = self.geocode(data["data"][key]["area"] + " Singapore")
                    if location is not None:
                        self.database_model.insert(
                            table.coordinate,
                            {
                                "area": data["data"][key]["area"],
                                "longitude": location.longitude,
                                "latitude": location.latitude,
                                "time": str(datetime.datetime.now()),
                            },
                        )
                        data["data"][key]["coordinate"] = self.database_model.query_one(
                            table.coordinate, area=data["data"][key]["area"]
                        )[0]
                    else:
                        data["data"][key]["coordinate"] = None
                        logger.logger.info(
                            "%s - %s", __name__, data["data"][key]["area"]
                        )
                else:
                    data["data"][key]["coordinate"] = None
        return data

    def get_info(self):
        info = {}
        with open(PATH + "/assets/SportSGSportFacilitiesGEOJSON.geojson") as file:
            data = json.load(file)

            for feature in data["features"]:
                name = feature["properties"]["Name"]
                info[name] = {}
                info[name]["geometry"] = feature["geometry"]["coordinates"][0][0]
                soup = BeautifulSoup(
                    feature["properties"]["Description"], features="html.parser"
                )
                keys = soup.find_all("th")[1:]
                values = soup.find_all("td")
                for i, key in enumerate(keys):
                    parsed_key = (
                        str(key).replace("<th>", "").replace("</th>", "").lower()
                    )
                    info[name][parsed_key] = (
                        str(values[i]).replace("<td>", "").replace("</td>", "").lower()
                    )
        return info

    def get_address(
        self,
        write_to_file=True,
        file_path=PATH + "/assets",
        file_name="activesgGymAddr",
        replace=False,
    ):
        active_sg = self.get_info()
        address = []
        address_file = file_path + "/" + file_name + ".txt"
        if os.path.isfile(address_file) and not replace:
            with open(address_file) as f:
                for line in f:
                    address.append(line.strip())
        else:
            with open(address_file, "w") as f:
                for key in active_sg:
                    if active_sg[key]["gym"]:
                        coordinate = active_sg[key]["geometry"]
                        locname = self.geo_locator.reverse(
                            f"{coordinate[1]}, {coordinate[0]}"
                        )
                        if write_to_file:
                            f.write(locname.address)
                            f.write(", ")
                            f.write(active_sg[key]["sports_cen"])
                            f.write(", ")
                            f.write(active_sg[key]["road_name"])
                            f.write("\n")
                        address.append(locname.address)
        return address


if __name__ == "__main__":
    a = GymCapacity()
    a.get_data()
