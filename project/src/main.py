from controller import weather, model, gymcapacity
from database import table
from logger import logger

if __name__ == "__main__":
    logger.logger.info('Started')
    a = weather.Weather()
    weatherData = a.getData()
    b = gymcapacity.gymCapacity()
    gymData = b.getData()
    address = b.getAddress()

    weatherIndex = {}
    for wData in weatherData:
        logger.logger.info(wData['area'])
        weatherIndex[wData['area']] = model.model.insert(table.weather, wData)
    for key in gymData['data']:
        GYMdata = {}
        GYMarea = key
        replace= ['ActiveSG','@','Gym','CC','East','West']
        for r in replace:
            GYMarea = GYMarea.replace(r, '')
        GYMarea = GYMarea.strip().lower()
        if gymData['data'][key].lower() == 'closed':
            GYMdata['capacity'] = 0
        else:
            GYMdata['capacity'] = int(gymData['data'][key].replace('%', '').replace('full', '').strip())
        GYMdata['created_at'] = gymData['timestamp']
        GYMdata['location'] = key
        for wData in weatherData:
            if GYMarea in wData['area'].lower() or wData['area'].lower() in GYMarea:
                GYMdata['weather_id'] = weatherIndex[wData['area']]
                break
            else:
                found = False
                for addr in address:
                    if GYMarea in addr:
                        if wData['area'].lower() in addr.lower():
                            GYMdata['weather_id'] = weatherIndex[wData['area']]
                            logger.logger.info("area : %s, %s", wData['area'], GYMarea)
                            found = True
                            break
                if found : break
        model.model.insert(table.gym_capacity, GYMdata)

    #     # print(model.model.insert(table.weather, data))
    model.model.queryAll(table.gym_capacity)