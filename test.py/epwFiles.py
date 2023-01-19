from epwFileProcess import*
import pandas as pd
from coolingLoadFunctions import*
def Create_df_weather(fileName, splitTab):

    #read_ewp_as_link(Link_weather)
    epw = EPW()
    if splitTab == True:
        epw.read_tab(fileName)
    else:
        epw.read(fileName)
    #print(epw.location.country)
    #lat = epw.location.latitude
    #print(epw.location.longitude)
    #print(epw.location.elevation)
    year = []
    month = []
    day = []
    date=[]
    hour = []
    seconde = []
    dry_bulb_temperature = []
    dew_point_temperature = []
    relative_humidity = []
    atmospheric_station_pressure = []
    global_horizontal_radiation = []
    direct_normal_radiation = []
    diffuse_horizontal_radiation = []
    wind_direction = []
    wind_speed = []
    total_sky_cover = []
    opaque_sky_cover = []
    precipitable_water = []
   
    for wd in epw.weatherdata:
        year.append(wd.year)
        month.append(wd.month)
        day.append(wd.day)
        hour.append(wd.hour)
        dry_bulb_temperature.append(wd.dry_bulb_temperature)
        dew_point_temperature.append(wd.dew_point_temperature)
        relative_humidity.append(wd.relative_humidity)
        atmospheric_station_pressure.append(wd.atmospheric_station_pressure)
        global_horizontal_radiation.append(wd.global_horizontal_radiation)
        direct_normal_radiation.append(wd.direct_normal_radiation)
        diffuse_horizontal_radiation.append(wd.global_horizontal_radiation)
        wind_direction.append(wd.wind_direction)
        wind_speed.append(wd.wind_speed)
        total_sky_cover.append(wd.total_sky_cover)
        opaque_sky_cover.append(wd.opaque_sky_cover)
        precipitable_water.append(wd.precipitable_water)

    averageRadiation = []

    for k in range(0,24-1):
        seasonDaySum = 0
        seasonDayAverage = 0
        for i in range(0,len(direct_normal_radiation)-24,24):
            seasonDaySum += direct_normal_radiation[k+i]
        seasonDayAverage = seasonDaySum/((len(direct_normal_radiation)-1)/24)
        for i in range(0,4):
            averageRadiation.append(seasonDayAverage)   
    temperature = []
    for k in range(0,24-1):
        seasonDaySum = 0
        seasonDayAverage = 0
        for i in range(0,len(dry_bulb_temperature)-24,24):
            seasonDaySum += dry_bulb_temperature[k+i]
        seasonDayAverage = seasonDaySum/((len(dry_bulb_temperature)-1)/24)
        for i in range(0,4):
            temperature.append(seasonDayAverage) 
           
        
    
    data_weather = pd.DataFrame(
        [year, month, day, hour, temperature, dry_bulb_temperature,  dew_point_temperature, relative_humidity,
         atmospheric_station_pressure, global_horizontal_radiation, direct_normal_radiation, diffuse_horizontal_radiation,
         averageRadiation, wind_direction,
         wind_speed, total_sky_cover, opaque_sky_cover, precipitable_water])
    
    data_weather = data_weather.transpose()
    data_weather.columns = ['year', 'month', 'day', 'hour','average_temperature', 'dry_bulb_temperature', 'dew_point_temperature',
                            'relative_humidity',
                            'atmospheric_station_pressure', 'global_horizontal_radiation', 'direct_normal_radiation',
                            'diffuse_horizontal_radiation', 'average_radiation',
                            'wind_direction', 'wind_speed', 'total_sky_cover', 'opaque_sky_cover', 'precipitable_water']
    

    return data_weather

