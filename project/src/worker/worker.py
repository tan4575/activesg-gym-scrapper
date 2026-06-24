#!/usr/bin/python3
import datetime
import os
import sys
from threading import Event

if __name__ == "__main__":
    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1, PATH)
from controller import gymcapacity, model, weather
from database import table
from logger import logger
from services import services


class ScrapingThread(services.Service):
    def __init__(
        self,
        group=None,
        target=None,
        name="ScrappingThread",
        timeout=10.0,
        args=...,
        kwargs=None,
        *,
        daemon=None,
    ):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._timeout_event_flag: Event = Event()
        self._timeout = timeout
        self._weather_instance = weather.Weather()
        self._gym_capacity_instance = gymcapacity.GymCapacity()

    def _start(self):
        self.start()

    def _stop(self):
        self.stop()

    def process_data(self):
        weather_data = self._weather_instance.get_data()
        gym_data = self._gym_capacity_instance.get_data()

        if len(weather_data) == 0 or len(gym_data) == 0:
            return

        weather_index = {}
        for weather_record in weather_data:
            logger.logger.info(weather_record)
            weather_index[weather_record["area"]] = model.model.insert(
                table.weather, weather_record
            )

        for gym_record in gym_data["data"]:
            gym_capacity_data = {}
            # Capacity
            if gym_data["data"][gym_record]["capacity"].lower() == "closed":
                gym_capacity_data["capacity"] = 0
            else:
                gym_capacity_data["capacity"] = int(
                    gym_data["data"][gym_record]["capacity"]
                    .replace("%", "")
                    .replace("full", "")
                    .strip()
                )

            # Timestamp
            gym_capacity_data["created_at"] = gym_data["timestamp"]

            # Locations
            gym_capacity_data["location"] = gym_data["data"][gym_record]["name"]

            # Find the closest weather coordinate.
            if gym_data["data"][gym_record]["coordinate"] is not None:
                gym_capacity_data["coordinate_id"] = gym_data["data"][gym_record][
                    "coordinate"
                ]["id"]
                distance = float("inf")
                best_match = ()
                for weather_record in weather_data:
                    coord_dist = self._weather_instance.haversine(
                        weather_record["latitude"],
                        weather_record["longitude"],
                        gym_data["data"][gym_record]["coordinate"]["latitude"],
                        gym_data["data"][gym_record]["coordinate"]["longitude"],
                    )
                    if coord_dist < distance:
                        distance = coord_dist
                        gym_capacity_data["weather_id"] = weather_index[
                            weather_record["area"]
                        ]
                        best_match = (
                            gym_data["data"][gym_record]["area"],
                            weather_record["area"],
                        )
                logger.logger.info("best match : %s, %s", best_match[0], best_match[1])
            model.model.insert(table.gym_capacity, gym_capacity_data)
        model.model.query_all(table.gym_capacity)

    def work_thread(self):
        current_time = datetime.datetime.now()
        if 7 <= current_time.hour <= 22:
            self.process_data()
        self.set_running()
        while self._running:
            self._timeout_event_flag.wait(self._timeout)
            self._timeout_event_flag.clear()
            current_time = datetime.datetime.now()
            if 7 <= current_time.hour <= 22:
                print(current_time)
                self.process_data()


ScrappingThread = ScrapingThread


if __name__ == "__main__":
    test = ScrapingThread()
    test._start()
    test.join()
