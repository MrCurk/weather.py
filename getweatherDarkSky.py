import json
import requests
from datetime import datetime
import cx_Oracle


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
    def __init__(self, country, name, lon, lat, timezone, date_time, weather, weather_icon, precipIntensity,
                 precipProbability, temperature, apparentTemperature, dewPoint, humidity, pressure, windSpeed, windGust,
                 windBearing, cloudCover, uvIndex, visibility, ozone, nearest_station, units, alert_title
                 , alert_description, alert_regions, alert_severity, alert_issued_time, alert_expires_time, forecast_summary):
        self.country = country
        self.timezone = timezone
        self.name = name
        self.lon = lon
        self.lat = lat
        self.date_time = date_time
        self.weather = weather
        self.weather_icon = weather_icon
        self.precipIntensity = precipIntensity
        self.precipProbability = precipProbability
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
        self.alert_title = alert_title
        self.alert_description = alert_description
        self.alert_regions = alert_regions
        self.alert_severity = alert_severity
        self.alert_issued_time = alert_issued_time
        self.alert_expires_time = alert_expires_time
        self.forecast_summary=forecast_summary

    def printData(self):
        print("country ", self.country)
        print("timezone ", self.timezone)
        print("name ", self.name)
        print("lon ", self.lon)
        print("lat ", self.lat)
        print("date_time ", self.date_time)
        print("weather ", self.weather)
        print("weather_icon ", self.weather_icon)
        print("precipIntensity ", self.precipIntensity)
        print("precipProbability ", self.precipProbability)
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
        print("alert_title ", self.alert_title)
        print("alert_description ", self.alert_description)
        print("alert_regions ", self.alert_regions)
        print("alert_severity ", self.alert_severity)
        print("alert_issued_time ", self.alert_issued_time)
        print("alert_expires_time ", self.alert_expires_time)
        print("forecast_summary ", self.forecast_summary)


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
def getCityWeather(country, name, latitude, longitude, appid):
    url = "https://api.darksky.net/forecast/{APPID}/{LATITUDE},{LONGITUDE}?exclude=minutely,hourly&units=si&lang=sl".format(
        APPID=appid, LATITUDE=str(latitude), LONGITUDE=str(longitude))

    response = requests.get(url)
    json_data = json.loads(response.text)
    cityWeather = CityWeather(country, name, getApiValue(json_data, "latitude"),
                getApiValue(json_data, "longitude"), getApiValue(json_data, "timezone"),
                getApiValue(json_data, "currently", "time"), getApiValue(json_data, "currently", "summary"),
                getApiValue(json_data, "currently", "icon"),
                getApiValue(json_data, "currently", "precipIntensity"),
                getApiValue(json_data, "currently", "precipProbability"),
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
                getApiValue(json_data, "flags", "nearest-station"), getApiValue(json_data, "flags", "units"),
                getApiValue(json_data, "alerts", "title"), getApiValue(json_data, "alerts", "description"),
                getApiValue(json_data, "alerts", "regions"), getApiValue(json_data, "alerts", "severity"),
                getApiValue(json_data, "alerts", "time"), getApiValue(json_data, "alerts", "expires"),
                getApiValue(json_data, "daily", "summary")
                )
    return  cityWeather
########################################################################################################################
# variables
# disable db connection for testing mode
db_NO_CONNECTION = True

########################################################################################################################
##  CONFIG PARAMETERS - geting data from config file
config_json = open("config.json").read()
config_data = json.loads(config_json)
# openWeather id
appid = config_data["APPID_DarkSky"]

# connection string
connection_string = config_data["DB_USERNAME"] + "/" + config_data["DB_PASSWORD"] + "@" + config_data["DB_TNS"]

# list of cities
city_list = list()
for item in config_data["City"]:
    city_list.append(City(item["name"], item["country"], item["latitude"], item["longitude"]))

########################################################################################################################
#cityWeather = list()

for city in city_list:
    # get weather data
    getCityWeather(city.country, city.name, city.latitude, city.longitude, appid).printData()



