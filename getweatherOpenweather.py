import json
import requests
from datetime import datetime
import cx_Oracle


########################################################################################################################
### WEATHER CLASS - part of CityWeather class, class for weather
class Weather:
    def __init__(self, id, main, description=None):
        self.id = id
        self.main = main
        self.description = description

    def printData(self):
        print("id={0}, main={1}, description={2}".format(self.id, self.main, self.description))


########################################################################################################################
### CITYWEATHER CLASS - openWeather api weather data for city
class CityWeather:
    def __init__(self, country=None, id=None, name=None, lon=None, lat=None, date_time=None, temp=None, pressure=None,
                 humidity=None, temp_min=None, temp_max=None, wind_speed=None, wind_deg=None, rain_1h=None,
                 rain_3h=None, snow_1h=None, snow_3h=None, clouds=None):
        self.country = country
        self.id = id
        self.name = name
        self.lon = lon
        self.lat = lat
        self.date_time = date_time
        self.temp = temp
        self.pressure = pressure
        self.humidity = humidity
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.wind_speed = wind_speed
        self.wind_deg = wind_deg
        self.rain_1h = rain_1h
        self.rain_3h = rain_3h
        self.snow_1h = snow_1h
        self.snow_3h = snow_3h
        self.clouds = clouds
        self.weather = list()

    # function for adding weather, it can be a list
    def addWeather(self, id, main, description=None):
        self.weather.append(Weather(id, main, description))

    # print data
    def printData(self):
        print("country = ", self.country)
        print("id = ", self.id)
        print("name = ", self.name)
        print("lon / lat = {0} / {1}".format(self.lon, self.lat))
        print("date_time = ", self.date_time)
        print("temp [temp_min / temp_max]= {0} [{1} / {2}]".format(self.temp, self.temp_min, self.temp_max))
        print("pressure = ", self.pressure)
        print("humidity = ", self.humidity)
        print("wind_speed [wind_deg] = {0} [{1}]".format(self.wind_speed, self.wind_deg))
        print("rain_1h / rain_3h = {0} / {1}".format(self.rain_1h, self.rain_3h))
        print("snow_1h / snow_3h = {0} / {1}".format(self.snow_1h, self.snow_3h))
        print("clouds = ", self.clouds)
        for item in self.weather:
            item.printData()


########################################################################################################################
### function try/catch if obj hasn't exist
def getApiValue(item, key1, key2=None):
    try:
        if key2 is None:
            return item[key1]
        else:
            return item[key1][key2]
    except(KeyError):
        return None

########################################################################################################################
# variables
# disable db connection for testing mode
db_NO_CONNECTION = True

########################################################################################################################
##  CONFIG PARAMETERS - geting data from config file
config_json = open("config.json").read()
config_data = json.loads(config_json)
# openWeather id
appid = config_data["APPID_OpenWeather"]

# connection string
connection_string = config_data["DB_USERNAME"] + "/" + config_data["DB_PASSWORD"] + "@" + config_data["DB_TNS"]

# list of cities
city_id_list = list()
for item in config_data["City"]:
    if item["id_OW"] > 0:
        city_id_list.append(str(item["id_OW"]))

city_ids = ",".join(city_id_list)
########################################################################################################################

# get weather data
url = "http://api.openweathermap.org/data/2.5/group?id={0}&units=metric&APPID={1}".format(city_ids, appid)
response = requests.get(url)
json_data = json.loads(response.text)

cityWeather = list()
i = 0
for item in json_data['list']:
    # append-create new object with  city weather data
    cityWeather.append(
        CityWeather(getApiValue(item, 'sys', 'country'),
                    getApiValue(item, 'id'),
                    getApiValue(item, 'name'),
                    getApiValue(item, 'coord', 'lon'),
                    getApiValue(item, 'coord', 'lat'),
                    datetime.utcfromtimestamp(getApiValue(item, 'dt')).strftime('%Y-%m-%d %H:%M:%S'),
                    getApiValue(item, 'main', 'temp'),
                    getApiValue(item, 'main', 'pressure'),
                    getApiValue(item, 'main', 'humidity'),
                    getApiValue(item, 'main', 'temp_min'),
                    getApiValue(item, 'main', 'temp_max'),
                    getApiValue(item, 'wind', 'speed'),
                    getApiValue(item, 'wind', 'deg'),
                    getApiValue(item, 'rain', '1h'),
                    getApiValue(item, 'rain', '3h'),
                    getApiValue(item, 'snow', '1h'),
                    getApiValue(item, 'snow', '3h'),
                    getApiValue(item, 'clouds', 'all')
                    ))
    # add weater to upper created object of city
    for item_weather in item['weather']:
        cityWeather[i].addWeather(
            getApiValue(item_weather, 'id'),
            getApiValue(item_weather, 'main'),
            getApiValue(item_weather, 'description')
        )

    i += 1

########################################################################################################################
# connect to db
if db_NO_CONNECTION == False:
    con = cx_Oracle.connect(connection_string)
    cursor = con.cursor()

for item_cityWeather in cityWeather:
    # item_cityWeather.printData()

    # max 4 weather condition for a city
    id1 = None
    main1 = None
    description1 = None
    id2 = None
    main2 = None
    description2 = None
    id3 = None
    main3 = None
    description3 = None
    id4 = None
    main4 = None
    description4 = None
    id5 = None
    main5 = None
    description5 = None
    multi_weather_in_5 = 0

    # set 1. weather condition
    if item_cityWeather.weather.__len__() >= 1:
        id1 = item_cityWeather.weather[0].id
        main1 = item_cityWeather.weather[0].main
        description1 = item_cityWeather.weather[0].description
    # set 2. weather condition
    if item_cityWeather.weather.__len__() >= 2:
        id2 = item_cityWeather.weather[1].id
        main2 = item_cityWeather.weather[1].main
        description2 = item_cityWeather.weather[1].description
    # set 3. weather condition
    if item_cityWeather.weather.__len__() >= 3:
        id3 = item_cityWeather.weather[2].id
        main3 = item_cityWeather.weather[2].main
        description3 = item_cityWeather.weather[2].description
    # set 4. weather condition
    if item_cityWeather.weather.__len__() == 4:
        id4 = item_cityWeather.weather[3].id
        main4 = item_cityWeather.weather[3].main
        description4 = item_cityWeather.weather[3].description

    # if are more then 4 weathers condition for a city, 5 and all next are joined together
    if item_cityWeather.weather.__len__() > 4:
        i = 0
        for weather in item_cityWeather.weather:
            i += 1
            if i == 5:
                id5 = str(item.id)
                main5 = str(item.main)
                description5 = str(item.description)
            elif i > 5:
                multi_weather_in_5 = 1
                id5 = id5 + ";" + str(item.id)
                main5 = main5 + ";" + str(item.main)
                description5 = description5 + ";" + str(item.description)

    if db_NO_CONNECTION == False:
        cursor.callproc('ADD_CITY_WEATHER',
                        [
                            item_cityWeather.country, item_cityWeather.id, item_cityWeather.name, item_cityWeather.lon,
                            item_cityWeather.lat, item_cityWeather.date_time, item_cityWeather.temp,
                            item_cityWeather.temp_min,
                            item_cityWeather.temp_max, item_cityWeather.pressure, item_cityWeather.humidity,
                            item_cityWeather.clouds,
                            item_cityWeather.wind_speed, item_cityWeather.wind_deg, item_cityWeather.rain_1h,
                            item_cityWeather.rain_3h,
                            item_cityWeather.snow_1h, item_cityWeather.snow_3h,
                            id1, main1, description1, id2, main2, description2, id3, main3, description3, id4, main4,
                            description4, id5, main5, description5, multi_weather_in_5
                        ])
    else:
        print(item_cityWeather.country, item_cityWeather.id, item_cityWeather.name, item_cityWeather.lon,
              item_cityWeather.lat, item_cityWeather.date_time, item_cityWeather.temp,
              item_cityWeather.temp_min,
              item_cityWeather.temp_max, item_cityWeather.pressure, item_cityWeather.humidity,
              item_cityWeather.clouds,
              item_cityWeather.wind_speed, item_cityWeather.wind_deg, item_cityWeather.rain_1h,
              item_cityWeather.rain_3h,
              item_cityWeather.snow_1h, item_cityWeather.snow_3h,
              id1, main1, description1, id2, main2, description2, id3, main3, description3, id4, main4,
              description4, id5, main5, description5, multi_weather_in_5
              )

if db_NO_CONNECTION == False:
    con.close()
