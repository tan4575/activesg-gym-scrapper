import os, sys
PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])

if __name__ == "__main__":
    sys.path.insert(1,PATH)

from web import scrapping
from model import model
from database import table
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from logger import logger
import json, datetime

class gymCapacity():
    def __init__(self):
        self.scrapper = scrapping.Scrapping('https://activesg.gov.sg/gym-capacity')
        self.geoLoc = Nominatim(user_agent="GetLoc")
        
    def getData(self):
        data = self.scrapper.getData()
        for k in data['data']:
            try:
                data['data'][k]['coordinate'] = model.model.queryOne(table.coordinate, area=data['data'][k]['area'])[0]
            except Exception as e:
                if str(e) == "Not Found!":
                    location = self.geoLoc.geocode(data['data'][k]['area'] + " Singapore")
                    if location is not None:
                         model.model.insert(table.coordinate,{
                             'area'     : data['data'][k]['area'],
                             'longitude': location.longitude,
                             'latitude' : location.latitude,
                             'time'     : str(datetime.datetime.now())
                         })
                    else:
                        data['data'][k]['coordinate'] = None
                        logger.logger.info("%s - %s", __name__ , data['data'][k]['area'])
        return data
    
    def getInfo(self):
        info = {}
        # Open and read the JSON file
        with open( (PATH + '/assets/SportSGSportFacilitiesGEOJSON.geojson'), 'r' ) as file:
            data = json.load(file)

            for d in data['features']:
                info[d['properties']['Name']] = {}
                info[d['properties']['Name']]['geometry'] = d["geometry"]["coordinates"][0][0]
                soup = BeautifulSoup(d['properties']['Description'], features="html.parser")
                keys = soup.find_all('th')[1:]
                data = soup.find_all('td')
                for i,key in enumerate(keys):
                    k = str(key).replace('<th>', '').replace('</th>', '').lower()
                    info[d['properties']['Name']][k] = str(data[i]).replace('<td>', '').replace('</td>', '').lower()
        return info
    
    def getAddress(self, writeToFile=True, filePath= PATH + '/assets', fileName='activesgGymAddr', replace=False):
        activeSG = self.getInfo()
        address = []
        if os.path.isfile((filePath + '/' + fileName + '.txt')) and not replace:
            with open( (filePath + '/' + fileName + '.txt'), 'r' ) as f:
                for d in f:
                    address.append(d.strip())
        else:
            with open( (filePath + '/' +fileName + '.txt'), 'w' ) as f:
                for k in activeSG:
                    if activeSG[k]['gym']:
                        locname = self.geoLoc.reverse(f"{activeSG[k]['geometry'][1]}, {activeSG[k]['geometry'][0]}")
                        if writeToFile:
                            f.write(locname.address)
                            f.write(', ')
                            f.write(activeSG[k]['sports_cen'])
                            f.write(', ')
                            f.write(activeSG[k]['road_name'])
                            f.write('\n')
                        address.append(locname.address)
        return address

if __name__ == "__main__":
    a = gymCapacity()
    a.getData()
