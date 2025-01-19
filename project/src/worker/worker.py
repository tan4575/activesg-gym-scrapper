#!/bin/bash/python3
import os,sys,datetime
from threading import Event,Timer
if __name__ == "__main__":
    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1,PATH)
from logger import logger
from error import error
from services import services
from controller import weather, model, gymcapacity
from database import table

class ScrappingThread(services.service):
    def __init__(self, group=None, target=None, name="ScrappingThread", timeout=60.0, args=..., kwargs=None, *, daemon=None):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._timeout_event_flag    : Event     = Event()
        self._timeout                           = timeout
        self._weatherInstance                   = weather.Weather()
        self._gymcapacityInstance               = gymcapacity.gymCapacity()

    def _start(self):
        self.start()

    def _stop(self):
        self.stop()

    def processData(self):
        weatherData = self._weatherInstance.getData()
        gymData = self._gymcapacityInstance.getData()

        if len(weatherData) == 0 or len(gymData) == 0: return

        weatherIndex = {}
        for wData in weatherData:
            logger.logger.info(wData)
            weatherIndex[wData['area']] = model.model.insert(table.weather, wData)

        for gData in gymData['data']:
            GYMdata = {}
            ## Capacity
            if gymData['data'][gData]['capacity'].lower() == 'closed':
                GYMdata['capacity'] = 0
            else:
                GYMdata['capacity'] = int(gymData['data'][gData]['capacity'].replace('%', '').replace('full', '').strip())

            ## Timestamp
            GYMdata['created_at']   = gymData['timestamp']

            ## locations
            GYMdata['location']     = gymData['data'][gData]['name']

            ## Find the closes distance to weather coordinate
            if gymData['data'][gData]['coordinate'] is not None:
                GYMdata['coordinate_id'] = gymData['data'][gData]['coordinate']['id']
                dist = float("inf")
                bestMatch = ()
                for wData in weatherData:
                    coord_dist = self._weatherInstance.haversine(wData["latitude"],
                                    wData["longitude"], 
                                    gymData['data'][gData]['coordinate']['latitude'],
                                    gymData['data'][gData]['coordinate']['longitude'])
                    if coord_dist < dist:
                        dist = coord_dist
                        ## weather_id
                        GYMdata['weather_id'] = weatherIndex[wData['area']]
                        bestMatch = gymData['data'][gData]['area'] , wData['area']
                logger.logger.info("best match : %s, %s", bestMatch[0], bestMatch[1])
            model.model.insert(table.gym_capacity, GYMdata)
        ## model.model.queryAll(table.gym_capacity)

    def work_thread(self):
        currentTime = datetime.datetime.now()
        if currentTime.hour <= 22 and currentTime.hour >= 7:
            self.processData()
        self.set_running()
        while self._running:
            self._timeout_event_flag.wait(self._timeout)
            self._timeout_event_flag.clear()
            currentTime = datetime.datetime.now()
            if currentTime.hour <= 22 and currentTime.hour >= 7:
                print(currentTime)
                self.processData()


if __name__ == "__main__":
    test = ScrappingThread()
    test._start()
    test.join()
