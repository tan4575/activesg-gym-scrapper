#!/bin/bash/python3
import requests, os, sys
from requests.exceptions import HTTPError
if __name__ == "__main__":
    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1,PATH)
from logger import logger

class sendRequest():
    
    def __init__(self):
        pass

    def getRequest(self, url, params=None):
        try:
            response = requests.get(url, params)
        except HTTPError as http_err:
            logger.logger.error("%s - HTTP error : %s", __name__ , http_err)
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.logger.error("%s - error : %s", __name__ , err)
            print(f"Other error occurred: {err}")
        else:
            if response.status_code == 200:
                return response.json()
            else:
                return 0

    def getRainFallData(self):
        data = dict()
        ret = self.getRequest("https://api-open.data.gov.sg/v2/real-time/api/rainfall")
        if len(ret) == 0 : return data
        for i in ret['data']['stations']:
            data[i['deviceId']] = {}
            data[i['deviceId']]['name'] = i['name']
            data[i['deviceId']]['location'] = i['location']
        for i in ret['data']['readings'][0]['data']:
            data[i['stationId']]['timestamp'] =  ret['data']['readings'][0]["timestamp"]
            data[i['stationId']]['value'] = i['value']
        return data

    def getAirTempData(self):
        data = dict()
        ret = self.getRequest("https://api-open.data.gov.sg/v2/real-time/api/air-temperature")

    def getTwoHourForecast(self):
        data = dict()
        ret = self.getRequest("https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast")
        if len(ret) == 0 : return data
        for i in ret['data']['area_metadata']:
            data[i['name']] = {}
            data[i['name']]['location'] = i['label_location']

        for i in ret['data']['items'][0]["forecasts"]:
            data[i['area']]['timestamp']  = ret['data']['items'][0]["timestamp"]
            data[i['area']]['forecast'] = i['forecast']
        return data

if __name__ == "__main__":
    t = sendRequest()
    
    r1 = t.getRainFallData()
    r2 = t.getTwoHourForecast()
    for k in r1.keys():
        for k1 in r2.keys():
            if k1 in r1[k]['location']:
                r1[k]['forecast'] = r2[k1]['forecast']
                break

    print(r1)
    # print(t.getRequest("https://api-open.data.gov.sg/v2/real-time/api/air-temperature"))
    # print(t.getRequest("https://api-open.data.gov.sg/v2/real-time/api/two-hr-forecast"))
    