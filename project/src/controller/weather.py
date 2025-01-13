import os, sys

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

    def getData(self):
        r1 = self.request.getRainFallData()
        r2 = self.request.getTwoHourForecast()
        retData = []
        for k in r1.keys():
            for k1 in r2.keys():
                if k1 in r1[k]['location']:
                    r1[k]['forecast'] = r2[k1]['forecast']
                    break
        for k in r1:
            data = {}
            data['deviceId'] = k
            if r1[k].get('location') is not None:
                data['area'] = r1[k]['location']
            if r1[k].get('value') is not None:
                data['rainfall'] = r1[k]['value']
            if r1[k].get('forecast') is not None:
                data['forecast'] = r1[k]['forecast']
            data['time'] = r1[k]['timestamp']
            retData.append(data)
        return retData

if __name__ == "__main__":
    a = Weather()
    for data in a.getData():
        model.model.insert(table.weather, data)
    model.model.queryAll(table.weather)