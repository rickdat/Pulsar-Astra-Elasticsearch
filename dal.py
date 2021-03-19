import requests
import json

class dal():
    
    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)


    def get_forecast(self, latitude: str, longitude: str):
        # get forecast url for latitude and longitude
        response = requests.get("https://api.weather.gov/points/" + latitude + "," + longitude)
        weatherdict = json.loads(response.text)
        propertiesdict = weatherdict["properties"]
        # get forecast url
        forecastreq = requests.get(propertiesdict["forecast"])
        # get forecast from url
        forecast = json.loads(forecastreq.text)
        self.forecast = forecast
        return forecast

    def get_forecast_description(self, element: int):
        forecast_list = self.forecast['properties']['periods']
        description_list = forecast_list[element]
        description = str(description_list["detailedForecast"])
        date = str(description_list["startTime"])
        return date, description


if __name__ == '__main__':
    forecastobj = dal()
    forecast = str(forecastobj.get_forecast(latitude= "38.8894", longitude= "-77.0352"))
    print(forecastobj.get_forecast_description(12))