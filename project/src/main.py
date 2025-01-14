from controller import weather, model, gymcapacity
from database import table
from logger import logger

if __name__ == "__main__":
    logger.logger.info('Started')
    a = weather.Weather()
    weatherData = a.getData()
    b = gymcapacity.gymCapacity()
    gymData = b.getData()

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
        GYMdata['location']     = gymData['data'][gData]['area']


        ## Find the closes distance to weather coordinate
        if gymData['data'][gData]['coordinate'] is not None:
            GYMdata['coordinate_id'] = gymData['data'][gData]['coordinate']['id']
            dist = float("inf")
            bestMatch = ()
            for wData in weatherData:
                coord_dist = a.haversine(wData["latitude"],
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
