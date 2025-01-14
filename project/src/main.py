from controller import weather, model, gymcapacity
from database import table
from logger import logger
import math

# haversine formula
def haversine(lat1, lon1, lat2, lon2):
     
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
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

if __name__ == "__main__":
    logger.logger.info('Started')
    a = weather.Weather()
    weatherData = a.getData()
    b = gymcapacity.gymCapacity()
    gymData = b.getData()

    weatherIndex = {}
    for wData in weatherData:
        logger.logger.info(wData['area'])
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
        GYMdata['location']     = gymData['data'][gData]['area']


        ## Find the closes distance to weather coordinate
        if gymData['data'][gData]['coordinate'] is not None:
            GYMdata['coordinate_id'] = gymData['data'][gData]['coordinate']['id']
            dist = float("inf")
            bestMatch = ()
            for wData in weatherData:
                coord_dist = haversine(wData["latitude"],
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
    model.model.queryAll(table.gym_capacity)

    # address = b.getAddress()
    # weatherIndex = {}
    # for wData in weatherData:
    #     logger.logger.info(wData['area'])
    #     weatherIndex[wData['area']] = model.model.insert(table.weather, wData)
    # for key in gymData['data']:
    #     GYMdata = {}
    #     GYMarea = key
    #     replace= ['ActiveSG','@','Gym','CC','East','West']
    #     for r in replace:
    #         GYMarea = GYMarea.replace(r, '')
    #     GYMarea = GYMarea.strip().lower()
    #     if gymData['data'][key].lower() == 'closed':
    #         GYMdata['capacity'] = 0
    #     else:
    #         GYMdata['capacity'] = int(gymData['data'][key].replace('%', '').replace('full', '').strip())
    #     GYMdata['created_at'] = gymData['timestamp']
    #     GYMdata['location'] = key
    #     for wData in weatherData:
    #         if GYMarea in wData['area'].lower() or wData['area'].lower() in GYMarea:
    #             GYMdata['weather_id'] = weatherIndex[wData['area']]
    #             break
    #         else:
    #             found = False
    #             for addr in address:
    #                 if GYMarea in addr:
    #                     if wData['area'].lower() in addr.lower():
    #                         GYMdata['weather_id'] = weatherIndex[wData['area']]
    #                         logger.logger.info("area : %s, %s", wData['area'], GYMarea)
    #                         found = True
    #                         break
    #             if found : break
    #     model.model.insert(table.gym_capacity, GYMdata)

    # #     # print(model.model.insert(table.weather, data))
    # model.model.queryAll(table.gym_capacity)