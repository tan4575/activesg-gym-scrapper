#!/bin/bash/python3
import os, sys
import math
if __name__ == "__main__":
    import os, sys
    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1,PATH)

from database import table
from httprequests import sendRequest
from model import model

class Weather():
    def __init__(self):
        self.request = sendRequest.sendRequest()

    # haversine formula
    @staticmethod
    def haversine( lat1, lon1, lat2, lon2):
        
        # distance between latitudes
        # and longitudes
        dLat = (lat2 - lat1) * math.pi / 180.0
        dLon = (lon2 - lon1) * math.pi / 180.0
    
        # convert to radians
        lat1 = (lat1) * math.pi / 180.0
        lat2 = (lat2) * math.pi / 180.0
    
        # apply formulae
        a = (pow(math.sin(dLat / 2), 2) +
            pow(math.sin(dLon / 2), 2) *
                math.cos(lat1) * math.cos(lat2))
        rad = 6371
        c = 2 * math.asin(math.sqrt(a))
        return rad * c


    def getData(self):
        r1 = self.request.getRainFallData()
        r2 = self.request.getTwoHourForecast()
        retData = []
        location = []
        bestmatch = ()
        if len(r1) == 0 or len(r2) == 0 :
            return retData
        for k in r1.keys():
            r1[k]['area'] = None
            dist = float("inf")
            for k1 in r2.keys():
                coord_dist = self.haversine(r2[k1]['location']["latitude"],
                                            r2[k1]['location']["longitude"],
                                            r1[k]['location']["latitude"],
                                            r1[k]['location']["longitude"])
                if coord_dist < dist:
                    dist = coord_dist
                    r1[k]['forecast'] = r2[k1]['forecast']
                    r1[k]['area'] = k1
                    bestmatch = r1[k]['location'],  r1[k]['name']  ,r2[k1]['location'], k1
            location.append(r1[k]['area'])
        for k in r1:
            data = {}
            data['deviceId'] = k
            if r1[k].get('name') is not None:
                data['area'] = r1[k]['name']
            if r1[k].get('value') is not None:
                data['rainfall'] = r1[k]['value']
            if r1[k].get('forecast') is not None:
                data['forecast'] = r1[k]['forecast']
            data['time'] = r1[k]['timestamp']
            data['longitude'] = r1[k]['location']['longitude']
            data['latitude'] = r1[k]['location']['latitude']
            retData.append(data)
        return retData

if __name__ == "__main__":
    a = Weather()
    for data in a.getData():
        model.model.insert(table.weather, data)
    model.model.queryAll(table.weather)