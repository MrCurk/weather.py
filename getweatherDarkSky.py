import json
import requests
from datetime import datetime
import cx_Oracle
import sys
import os


########################################################################################################################
# CLASS
########################################################################################################################
### CITY CLASS
class City:
    def __init__(self, name, country, latitude, longitude):
        self.name = subString(name, 16)
        self.country = subString(country, 2)
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
                 windBearing, cloudCover, uvIndex, visibility, ozone, nearest_station, units, forecast_summary,
                 nearestStormBearing, nearestStormDistance, precipIntensityError, cityForecast=None, alert_list=None):
        self.country = country
        self.name = name
        self.lat = lat
        self.lon = lon
        self.timezone = timezone
        self.date_time = convertUnixTime2String(date_time)
        self.weather = subString(weather, 50)
        self.weather_icon = subString(weather_icon, 20)
        self.precipIntensity = precipIntensity
        self.precipProbability = precipProbability
        self.precipType = subString(precipType, 20)
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
        self.forecast_summary = subString(forecast_summary, 150)
        self.nearestStormBearing = nearestStormBearing
        self.nearestStormDistance = nearestStormDistance
        self.precipIntensityError = precipIntensityError
        self.cityForecast = cityForecast
        self.alert_list = alert_list

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
        print("nearestStormBearing ", self.nearestStormBearing)
        print("nearestStormDistance ", self.nearestStormDistance)
        print("precipIntensityError ", self.precipIntensityError)
        for item_forecast in self.cityForecast:
            item_forecast.printData()
        for item_alert in self.alert_list:
            item_alert.printData()


########################################################################################################################
### CITYALERT CLASS
class CityAlert:
    def __init__(self, title, region, severity, date_time, timezone, expires, description, uri):
        self.title = subString(title, 100)
        self.region = subString(region, 60)
        self.severity = severity
        self.date_time = convertUnixTime2String(date_time)
        self.timezone = timezone
        self.expires = convertUnixTime2String(expires)
        self.description = subString(description, 250)
        self.uri = subString(uri, 200)

    def printData(self):
        print("title ", self.title)
        print("regions ", self.region)
        print("severity ", self.severity)
        print("date_time ", self.date_time)
        print("timezone ", self.timezone)
        print("expires ", self.expires)
        print("description ", self.description)
        print("uri ", self.uri)


########################################################################################################################
### CITYFORECAST_DAILY CLASS
class CityForecastDaily:
    def __init__(self, name, country, latitude, longitude, date_time, timezone, weather, weather_icon, sunriseTime,
                 sunsetTime,
                 moonPhase, precipIntensity, precipIntensityMax, precipIntensityMaxTime, precipProbability,
                 precipAccumulation,
                 precipType, temperatureHigh, temperatureHighTime, temperatureLow, temperatureLowTime,
                 apparentTemperatureHigh,
                 apparentTemperatureHighTime, apparentTemperatureLow, apparentTemperatureLowTime, dewPoint, humidity,
                 pressure, windSpeed, windGust, windGustTime, windBearing, cloudCover, uvIndex, uvIndexTime, visibility,
                 ozone, precipIntensityError, nearest_station, units):
        self.name = name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.date_time = convertUnixTime2String(date_time)
        self.timezone = timezone
        self.weather = subString(weather, 200)
        self.weather_icon = subString(weather_icon, 20)
        self.sunriseTime = convertUnixTime2String(sunriseTime)
        self.sunsetTime = convertUnixTime2String(sunsetTime)
        self.moonPhase = moonPhase
        self.precipIntensity = precipIntensity
        self.precipIntensityMax = precipIntensityMax
        self.precipIntensityMaxTime = convertUnixTime2String(precipIntensityMaxTime)
        self.precipProbability = precipProbability
        self.precipAccumulation = precipAccumulation
        self.precipType = subString(precipType, 20)
        self.temperatureHigh = temperatureHigh
        self.temperatureHighTime = convertUnixTime2String(temperatureHighTime)
        self.temperatureLow = temperatureLow
        self.temperatureLowTime = convertUnixTime2String(temperatureLowTime)
        self.apparentTemperatureHigh = apparentTemperatureHigh
        self.apparentTemperatureHighTime = convertUnixTime2String(apparentTemperatureHighTime)
        self.apparentTemperatureLow = apparentTemperatureLow
        self.apparentTemperatureLowTime = convertUnixTime2String(apparentTemperatureLowTime)
        self.dewPoint = dewPoint
        self.humidity = humidity
        self.pressure = pressure
        self.windSpeed = windSpeed
        self.windGust = windGust
        self.windGustTime = convertUnixTime2String(windGustTime)
        self.windBearing = windBearing
        self.cloudCover = cloudCover
        self.uvIndex = uvIndex
        self.uvIndexTime = convertUnixTime2String(uvIndexTime)
        self.visibility = visibility
        self.ozone = ozone
        self.precipIntensityError = precipIntensityError
        self.nearest_station = nearest_station
        self.units = units

    def printData(self):
        print("name ", self.name)
        print("country ", self.country)
        print("lat ", self.latitude)
        print("lon ", self.longitude)
        print("date_time ", self.date_time)
        print("time zone ", self.timezone)
        print("weather ", self.weather)
        print("weather_icon ", self.weather_icon)
        print("sunriseTime ", self.sunriseTime)
        print("sunsetTime ", self.sunsetTime)
        print("moonPhase ", self.moonPhase)
        print("precipIntensity ", self.precipIntensity)
        print("precipIntensityMax ", self.precipIntensityMax)
        print("precipIntensityMaxTime ", self.precipIntensityMaxTime)
        print("precipProbability ", self.precipProbability)
        print("precipAccumulation ", self.precipAccumulation)
        print("precipType ", self.precipType)
        print("temperatureHigh ", self.temperatureHigh)
        print("temperatureHighTime ", self.temperatureHighTime)
        print("temperatureLow ", self.temperatureLow)
        print("temperatureLowTime ", self.temperatureLowTime)
        print("apparentTemperatureHigh ", self.apparentTemperatureHigh)
        print("apparentTemperatureHighTime ", self.apparentTemperatureHighTime)
        print("apparentTemperatureLow ", self.apparentTemperatureLow)
        print("apparentTemperatureLowTime ", self.apparentTemperatureLowTime)
        print("dewPoint ", self.dewPoint)
        print("humidity ", self.humidity)
        print("pressure ", self.pressure)
        print("windSpeed ", self.windSpeed)
        print("windGust ", self.windGust)
        print("windGustTime ", self.windGustTime)
        print("windBearing ", self.windBearing)
        print("cloudCover ", self.cloudCover)
        print("uvIndex ", self.uvIndex)
        print("uvIndexTime ", self.uvIndexTime)
        print("visibility ", self.visibility)
        print("ozone ", self.ozone)
        print("precipIntensityError ", self.precipIntensityError)
        print("nearest_station ", self.nearest_station)
        print("units ", self.units)


########################################################################################################################
# FUNCTION
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
### function cut string if it is longer then specific length
def subString(string, length):
    substring = None
    if string is not None:
        if len(string) <= length:
            substring = string
        else:
            if length >= 5:
                substring = string[0:(length - 3)] + "..."
            else:
                substring = string[0:length]

    return substring


########################################################################################################################
### function print log
def printLog(text, value=None, value1=None, value2=None, value3=None):
    utcnow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    now = datetime.now().strftime('%H:%M:%S')
    string4print = None
    if value is None:
        string4print = "{0}({1}) / {2}".format(utcnow, now, text)
    elif value1 is None:
        string4print = "{0}({1}) / {2} / {3}".format(utcnow, now, text, value)
    elif value2 is None:
        string4print = "{0}({1}) / {2} / {3} / {4}".format(utcnow, now, text, value, value1)
    elif value3 is None:
        string4print = "{0}({1}) / {2} / {3} / {4} / {5}".format(utcnow, now, text, value, value1, value2)
    else:
        string4print = "{0}({1}) / {2} / {3} / {4} / {5} / {6}".format(utcnow, now, text, value, value1, value2, value3)

    print(string4print)


########################################################################################################################
### function convert unix time to string format yyyy-mm-dd hh24:mi:si
def convertUnixTime2String(unixTime):
    datetimeString = None
    if unixTime is not None:
        datetimeString = datetime.utcfromtimestamp(unixTime).strftime('%Y-%m-%d %H:%M:%S')

    return datetimeString


########################################################################################################################
# function to fetch weather data from DarkSky web page
def fetchCityWeather(country, name, latitude, longitude, appid):
    url = "https://api.darksky.net/forecast/{APPID}/{LATITUDE},{LONGITUDE}?exclude=minutely,hourly&units=si".format(
        APPID=appid, LATITUDE=str(latitude), LONGITUDE=str(longitude))

    printLog("fatching data", name)
    response = requests.get(url)
    json_data = json.loads(response.text)

    # get time zone, needed in multiple parts
    timeZone = getApiValue(json_data, "timezone")

    # forecast list
    cityForecast_list = list()
    if getApiValue(json_data, "daily", "data") is not None:
        for item in getApiValue(json_data, "daily", "data"):
            cityForecast_list.append(CityForecastDaily(name, country, latitude, longitude,
                                                       getApiValue(item, "time"),
                                                       timeZone,
                                                       getApiValue(item, "summary"),
                                                       getApiValue(item, "icon"),
                                                       getApiValue(item, "sunriseTime"),
                                                       getApiValue(item, "sunsetTime"),
                                                       getApiValue(item, "moonPhase"),
                                                       getApiValue(item, "precipIntensity"),
                                                       getApiValue(item, "precipIntensityMax"),
                                                       getApiValue(item, "precipIntensityMaxTime"),
                                                       getApiValue(item, "precipProbability"),
                                                       getApiValue(item, "precipAccumulation"),
                                                       getApiValue(item, "precipType"),
                                                       getApiValue(item, "temperatureHigh"),
                                                       getApiValue(item, "temperatureHighTime"),
                                                       getApiValue(item, "temperatureLow"),
                                                       getApiValue(item, "temperatureLowTime"),
                                                       getApiValue(item, "apparentTemperatureHigh"),
                                                       getApiValue(item, "apparentTemperatureHighTime"),
                                                       getApiValue(item, "apparentTemperatureLow"),
                                                       getApiValue(item, "apparentTemperatureLowTime"),
                                                       getApiValue(item, "dewPoint"),
                                                       getApiValue(item, "humidity"),
                                                       getApiValue(item, "pressure"),
                                                       getApiValue(item, "windSpeed"),
                                                       getApiValue(item, "windGust"),
                                                       getApiValue(item, "windGustTime"),
                                                       getApiValue(item, "windBearing"),
                                                       getApiValue(item, "cloudCover"),
                                                       getApiValue(item, "uvIndex"),
                                                       getApiValue(item, "uvIndexTime"),
                                                       getApiValue(item, "visibility"),
                                                       getApiValue(item, "ozone"),
                                                       getApiValue(item, "precipIntensityError"),
                                                       getApiValue(json_data, "flags", "nearest-station"),
                                                       getApiValue(json_data, "flags", "units")))
    # alerts list
    alert_list = list()
    # loop through alerts
    if getApiValue(json_data, "alerts") is not None:
        for alert in getApiValue(json_data, "alerts"):
            title = getApiValue(alert, "title")
            time = getApiValue(alert, "time")
            severity = getApiValue(alert, "severity")
            expires = getApiValue(alert, "expires")
            description = getApiValue(alert, "description")
            uri = getApiValue(alert, "uri")

            # loop through regions in one alert
            for region in getApiValue(alert, "regions"):
                # create alert for each region
                alert_list.append(CityAlert(title, region, severity, time, timeZone, expires, description, uri))

    cityWeather = CityWeather(country, name,
                              getApiValue(json_data, "latitude"),
                              getApiValue(json_data, "longitude"),
                              timeZone,
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
                              getApiValue(json_data, "daily", "summary"),
                              getApiValue(json_data, "currently", "nearestStormBearing"),
                              getApiValue(json_data, "currently", "nearestStormDistance"),
                              getApiValue(json_data, "currently", "precipIntensityError"),
                              cityForecast_list,
                              alert_list
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
# PROGRAM
########################################################################################################################
##  CONFIG PARAMETERS - geting data from config file
## full path of config file
if len(sys.argv) > 1:
    config_full_path = sys.argv[1]
else:
    config_full_path = None

## read config file
if config_full_path != None:
    config_json = open(config_full_path).read()
else:
    config_json = open("config.json").read()

config_data = json.loads(config_json)

## config proxy
# get proxy data from config
proxyType = config_data["PROXY_TYPE"]
proxy = config_data["PROXY"]
proxyPort = config_data["PROXY_PORT"]
proxyUsername = config_data["PROXY_USERNAME"]
proxyPassword = config_data["PROXY_PASSWORD"]
proxyString = None
# set proxy string
if len(proxyType) > 0:
    if len(proxyUsername) == 0 and len(proxyPassword) == 0:
        proxyString = proxyType + "://" + proxy + ":" + proxyPort
    else:
        proxyString = proxyType + "://" + proxyUsername + ":" + proxyPassword + "@" + proxy + ":" + proxyPort
    # set proxy
    os.environ['http_proxy'] = proxyString
    os.environ['HTTP_PROXY'] = proxyString
    os.environ['https_proxy'] = proxyString
    os.environ['HTTPS_PROXY'] = proxyString

# DarkSky appid
appid = config_data["APPID_DarkSky"]

# test mode, without db connection == True
test_mode_no_db = str_to_bool(config_data["test_mode_no_db"])

# connection string
dbTns = config_data["DB_TNS"]
connection_string = None
if len(dbTns) == 0:
    connection_string = config_data["DB_USERNAME"] + "/" + config_data["DB_PASSWORD"]
else:
    connection_string = config_data["DB_USERNAME"] + "/" + config_data["DB_PASSWORD"] + "@" + config_data["DB_TNS"]

# list of cities
city_list = list()
for item in config_data["City"]:
    city_list.append(City(item["name"], item["country"], item["latitude"], item["longitude"]))

########################################################################################################################
# create a list of city with weather data
cityWeather = list()
for city in city_list:
    # get weather data from web
    cityWeather.append(fetchCityWeather(city.country, city.name, city.latitude, city.longitude, appid))

# connect to db, when not in test mode
con = None
cursor = None
if not test_mode_no_db:
    con = cx_Oracle.connect(connection_string)
    cursor = con.cursor()

# loop through list of cities weather
for item in cityWeather:
    # inserting into db
    if not test_mode_no_db:
        printLog("inserting data weather current", item.name)
        cursor.callproc('ADD_CITY_WEATHER',
                        [item.country, item.name, item.lat, item.lon, item.timezone, item.date_time, item.weather,
                         item.weather_icon, item.precipIntensity,
                         item.precipProbability, item.precipType, item.temperature, item.apparentTemperature,
                         item.dewPoint, item.humidity, item.pressure, item.windSpeed, item.windGust,
                         item.windBearing, item.cloudCover, item.uvIndex, item.visibility, item.ozone,
                         item.nearest_station, item.units, item.forecast_summary, item.nearestStormBearing,
                         item.nearestStormDistance, item.precipIntensityError
                         ])
        print()

        # inserting forecast
        for forecast in item.cityForecast:
            printLog("inserting data forecast ", item.name, "utc", forecast.date_time)
            cursor.callproc('ADD_WEATHER_DAILY_FORECAST',
                            [forecast.name, forecast.country, forecast.latitude, forecast.longitude, forecast.date_time,
                             forecast.timezone, forecast.weather, forecast.weather_icon, forecast.sunriseTime,
                             forecast.sunsetTime,
                             forecast.moonPhase, forecast.precipIntensity, forecast.precipIntensityMax,
                             forecast.precipIntensityMaxTime, forecast.precipProbability,
                             forecast.precipAccumulation,
                             forecast.precipType, forecast.temperatureHigh, forecast.temperatureHighTime,
                             forecast.temperatureLow, forecast.temperatureLowTime,
                             forecast.apparentTemperatureHigh,
                             forecast.apparentTemperatureHighTime, forecast.apparentTemperatureLow,
                             forecast.apparentTemperatureLowTime, forecast.dewPoint, forecast.humidity,
                             forecast.pressure, forecast.windSpeed, forecast.windGust, forecast.windGustTime,
                             forecast.windBearing, forecast.cloudCover, forecast.uvIndex, forecast.uvIndexTime,
                             forecast.visibility, forecast.ozone, forecast.precipIntensityError,
                             forecast.nearest_station, forecast.units])
        if len(item.cityForecast) > 0:
            printLog("End *****************")

        # inserting alerts
        for alert in item.alert_list:
            printLog("inserting data alert ", item.name, "utc", alert.date_time)
            # insert alerts
            cursor.callproc('ADD_WEATHER_ALERT',
                            [alert.title, alert.region, alert.severity, alert.date_time, alert.timezone, alert.expires,
                             alert.description, alert.uri])
            # insert region2city relations
            printLog("inserting region2city relations ", item.name, "utc", alert.date_time)
            cursor.callproc('ADD_WEATHER_CITY2REGION', [alert.region, item.name, item.lat, item.lon])
        if len(item.alert_list) > 0:
            printLog("End *****************")

        # end for one city
        printLog("End *****************", item.name)
        print()
    # testing mode only print
    else:
        print(item.country, item.name, item.lat, item.lon, item.timezone, item.date_time, item.weather,
              item.weather_icon, item.precipIntensity,
              item.precipProbability, item.precipType, item.temperature, item.apparentTemperature,
              item.dewPoint, item.humidity, item.pressure, item.windSpeed, item.windGust,
              item.windBearing, item.cloudCover, item.uvIndex, item.visibility, item.ozone,
              item.nearest_station, item.units, item.forecast_summary, item.nearestStormBearing,
              item.nearestStormDistance, item.precipIntensityError
              )
        for forecast in item.cityForecast:
            printLog("inserting data forecast ", item.name, "utc", forecast.date_time, forecast.precipIntensityError)
            print(forecast.date_time, forecast.weather)
        for alert in item.alert_list:
            printLog("inserting data alert ", item.name, "utc", alert.date_time)
            print(alert.date_time, alert.title)
            print(alert.region, item.name, item.lat, item.lon)
        print()

# close db connection
if not test_mode_no_db:
    con.close()
