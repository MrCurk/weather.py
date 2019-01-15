import json
import requests
from datetime import datetime
import cx_Oracle
import sys

########################################################################################################################
### CITY CLASS
class City:
    def __init__(self, name, country, latitude, longitude):
        self.name = name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

    def printData(self):
        print("name={0}, country,={1}, latitude={2}, longitude={3}".format(self.name, self.country, self.latitude,
                                                                           self.longitude))


########################################################################################################################
### CITYWEATHER CLASS - Dark Sky api weather data for city
class CityWeather(object):
    def __init__(self, country, name, lat, lon, timezone, date_time, weather, weather_icon, precipIntensity,
                 precipProbability, precipType, temperature, apparentTemperature, dewPoint, humidity, pressure,
                 windSpeed, windGust,
                 windBearing, cloudCover, uvIndex, visibility, ozone, nearest_station, units, forecast_summary):
        self.country = country
        self.name = name
        self.lat = lat
        self.lon = lon
        self.timezone = timezone
        self.date_time = datetime.utcfromtimestamp(date_time).strftime('%Y-%m-%d %H:%M:%S')
        self.weather = weather
        self.weather_icon = weather_icon
        self.precipIntensity = precipIntensity
        self.precipProbability = precipProbability
        self.precipType = precipType
        self.temperature = temperature
        self.apparentTemperature = apparentTemperature
        self.dewPoint = dewPoint
        self.humidity = humidity
        self.pressure = pressure
        self.windSpeed = windSpeed
        self.windGust = windGust
        self.windBearing = windBearing
        self.cloudCover = cloudCover
        self.uvIndex = uvIndex
        self.visibility = visibility
        self.ozone = ozone
        self.nearest_station = nearest_station
        self.units = units
        self.forecast_summary =  forecast_summary if len(forecast_summary) <=150  else forecast_summary[1:150]

    def printData(self):
        print("country ", self.country)
        print("timezone ", self.timezone)
        print("name ", self.name)
        print("lat ", self.lat)
        print("lon ", self.lon)
        print("date_time ", self.date_time)
        print("weather ", self.weather)
        print("weather_icon ", self.weather_icon)
        print("precipIntensity ", self.precipIntensity)
        print("precipProbability ", self.precipProbability)
        print("precipType ", self.precipType)
        print("temperature ", self.temperature)
        print("apparentTemperature ", self.apparentTemperature)
        print("dewPoint ", self.dewPoint)
        print("humidity ", self.humidity)
        print("pressure ", self.pressure)
        print("windSpeed ", self.windSpeed)
        print("windGust ", self.windGust)
        print("windBearing ", self.windBearing)
        print("cloudCover ", self.cloudCover)
        print("uvIndex ", self.uvIndex)
        print("visibility ", self.visibility)
        print("ozone ", self.ozone)
        print("nearest_station ", self.nearest_station)
        print("units ", self.units)
        print("forecast_summary ", self.forecast_summary)


########################################################################################################################
### CITYFORECAST_DAILY CLASS
class CityForecastDaily:
    def __init__(self, name, country, latitude, longitude, date_time, weather, weather_icon, sunriseTime, sunsetTime,
                 moonPhase, precipIntensity, precipIntensityMax, precipIntensityMaxTime, precipProbability,
                 precipAccumulation,
                 precipType, temperatureHigh, temperatureHighTime, temperatureLow, temperatureLowTime,
                 apparentTemperatureHigh,
                 apparentTemperatureHighTime, apparentTemperatureLow, apparentTemperatureLowTime, dewPoint, humidity,
                 pressure, windSpeed, windGust, windGustTime, windBearing, cloudCover, uvIndex, uvIndexTime, visibility,
                 ozone, temperatureMin, temperatureMinTime, temperatureMax, temperatureMaxTime, apparentTemperatureMin,
                 apparentTemperatureMinTime, apparentTemperatureMax, apparentTemperatureMaxTime):
        self.name = name,
        self.country = country,
        self.lat = latitude,
        self.lon = longitude,
        self.date_time = date_time,
        self.weather = weather,
        self.weather_icon = weather_icon,
        self.sunriseTime = sunriseTime,
        self.sunsetTime = sunsetTime,
        self.moonPhase = moonPhase,
        self.precipIntensity = precipIntensity,
        self.precipIntensityMax = precipIntensityMax,
        self.precipIntensityMaxTime = precipIntensityMaxTime,
        self.precipProbability = precipProbability,
        self.precipAccumulation = precipAccumulation,
        self.precipType = precipType,
        self.temperatureHigh = temperatureHigh,
        self.temperatureHighTime = temperatureHighTime,
        self.temperatureLow = temperatureLow,
        self.temperatureLowTime = temperatureLowTime,
        self.apparentTemperatureHigh = apparentTemperatureHigh,
        self.apparentTemperatureHighTime = apparentTemperatureHighTime,
        self.apparentTemperatureLow = apparentTemperatureLow,
        self.apparentTemperatureLowTime = apparentTemperatureLowTime,
        self.dewPoint = dewPoint,
        self.humidity = humidity,
        self.pressure = pressure,
        self.windSpeed = windSpeed,
        self.windGust = windGust,
        self.windGustTime = windGustTime,
        self.windBearing = windBearing,
        self.cloudCover = cloudCover,
        self.uvIndex = uvIndex,
        self.uvIndexTime = uvIndexTime,
        self.visibility = visibility,
        self.ozone = ozone,
        self.temperatureMin = temperatureMin,
        self.temperatureMinTime = temperatureMinTime,
        self.temperatureMax = temperatureMax,
        self.temperatureMaxTime = temperatureMaxTime,
        self.apparentTemperatureMin = apparentTemperatureMin,
        self.apparentTemperatureMinTime = apparentTemperatureMinTime,
        self.apparentTemperatureMax = apparentTemperatureMax,
        self.apparentTemperatureMaxTime = apparentTemperatureMaxTime

    def printData(self):
        print("TODO")


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
### function print log
def printLog(text, value):
    utcnow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    now = datetime.now().strftime('%H:%M:%S')
    print("{0}({1}) / {2} / {3}".format(utcnow, now, text, value))


########################################################################################################################
# function to fetch weather data from DarkSky web page
def fetchCityWeather(country, name, latitude, longitude, appid):
    url = "https://api.darksky.net/forecast/{APPID}/{LATITUDE},{LONGITUDE}?exclude=minutely,hourly&units=si".format(
        APPID=appid, LATITUDE=str(latitude), LONGITUDE=str(longitude))
    printLog("fatching data", name)
    response = requests.get(url)
    json_data = json.loads(response.text)
    cityWeather = CityWeather(country, name,
                              getApiValue(json_data, "latitude"),
                              getApiValue(json_data, "longitude"),
                              getApiValue(json_data, "timezone"),
                              getApiValue(json_data, "currently", "time"),
                              getApiValue(json_data, "currently", "summary"),
                              getApiValue(json_data, "currently", "icon"),
                              getApiValue(json_data, "currently", "precipIntensity"),
                              getApiValue(json_data, "currently", "precipProbability"),
                              getApiValue(json_data, "currently", "precipType"),
                              getApiValue(json_data, "currently", "temperature"),
                              getApiValue(json_data, "currently", "apparentTemperature"),
                              getApiValue(json_data, "currently", "dewPoint"),
                              getApiValue(json_data, "currently", "humidity"),
                              getApiValue(json_data, "currently", "pressure"),
                              getApiValue(json_data, "currently", "windSpeed"),
                              getApiValue(json_data, "currently", "windGust"),
                              getApiValue(json_data, "currently", "windBearing"),
                              getApiValue(json_data, "currently", "cloudCover"),
                              getApiValue(json_data, "currently", "uvIndex"),
                              getApiValue(json_data, "currently", "visibility"),
                              getApiValue(json_data, "currently", "ozone"),
                              getApiValue(json_data, "flags", "nearest-station"),
                              getApiValue(json_data, "flags", "units"),
                              getApiValue(json_data, "daily", "summary")
                              )
    return cityWeather


########################################################################################################################
# string to boolean
def str_to_bool(s):
    if s.upper() == 'TRUE':
        return True
    elif s.upper() == 'FALSE':
        return False
    else:
        raise ValueError


########################################################################################################################
##  CONFIG PARAMETERS - geting data from config file
config_full_path = sys.argv[1]

if config_full_path != None:
    config_json = open(config_full_path).read()
else:
    config_json = open("config.json").read()

config_data = json.loads(config_json)

# DarkSky appid
appid = config_data["APPID_DarkSky"]

# test mode, without db connection == True
test_mode_no_db = str_to_bool(config_data["test_mode_no_db"])

# connection string
connection_string = config_data["DB_USERNAME"] + "/" + config_data["DB_PASSWORD"] + "@" + config_data["DB_TNS"]

# list of cities
city_list = list()
for item in config_data["City"]:
    city_list.append(City(item["name"], item["country"], item["latitude"], item["longitude"]))

########################################################################################################################
cityWeather = list()
# create a list of city with weather data
for city in city_list:
    # get weather data
    cityWeather.append(fetchCityWeather(city.country, city.name, city.latitude, city.longitude, appid))

# connect to db, when not in test mode
con = None
cursor = None
if test_mode_no_db == False:
    con = cx_Oracle.connect(connection_string)
    cursor = con.cursor()

# loop through list of citys weather
for item in cityWeather:
    # inserting into db
    if test_mode_no_db == False:
        printLog("inserting data", item.name)
        cursor.callproc('ADD_CITY_WEATHER',
                        [item.country, item.name, item.lat, item.lon, item.timezone, item.date_time, item.weather,
                         item.weather_icon, item.precipIntensity,
                         item.precipProbability, item.precipType, item.temperature, item.apparentTemperature,
                         item.dewPoint, item.humidity, item.pressure, item.windSpeed, item.windGust,
                         item.windBearing, item.cloudCover, item.uvIndex, item.visibility, item.ozone,
                         item.nearest_station, item.units, item.forecast_summary])
    # testing mode only print
    else:
        print(item.country, item.name, item.lat, item.lon, item.timezone, item.date_time, item.weather,
              item.weather_icon, item.precipIntensity,
              item.precipProbability, item.precipType, item.temperature, item.apparentTemperature,
              item.dewPoint, item.humidity, item.pressure, item.windSpeed, item.windGust,
              item.windBearing, item.cloudCover, item.uvIndex, item.visibility, item.ozone,
              item.nearest_station, item.units, item.forecast_summary)

# close db connection
if test_mode_no_db == False:
    con.close()
