import requests
import json
import os
import time


CFG_PATH = os.path.join(os.path.dirname(__file__), 'states.json')


class dal():

    def jprint(self, obj):
        # create a formatted string of the Python JSON object
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def get_forecast(self, latitude: str, longitude: str, state: str):
        # get forecast url for latitude and longitude
        response = requests.get("https://api.weather.gov/points/" + str(latitude) + "," + str(longitude))
        weatherdict = json.loads(response.text)
        time.sleep(1)
        propertiesdict = weatherdict["properties"]
        # get forecast url
        if propertiesdict["forecast"]:
            forecastreq = requests.get(propertiesdict["forecast"])
            self.forecast = json.loads(forecastreq.text)
        else:
            print("No forecast")
            return
        # get forecast from url
        self.state = str(state)
        return self.forecast

    def get_forecast_description(self, element: int, latitude: str, longitude: str, state: str):
        cnt = 0
        while True:
            try:
                self.get_forecast(latitude=latitude, longitude=longitude, state=state)
                forecast_list = self.forecast['properties']['periods']
                description_list = forecast_list[element]
                description = self.state + ": " + str(description_list["detailedForecast"])
                date = str(description_list["startTime"])
                return date, description
            except:
                cnt = cnt + 1
                print(self.forecast)
                print("Goverment API forecast unavailable" + ", retrying")
                if cnt > 3:
                    print("No forecast available")
                    return "2021-03-27T06:00:00-04:00", "No forecast"
                    break
                continue
            cnt = 0
            break


    def get_states(self):
        with open(CFG_PATH) as f:
            data = json.load(f)
        return data



        # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
        #print( person_dict)

        # Output: ['English', 'French']
        #print(person_dict['languages'])


if __name__ == '__main__':
    forecastobj = dal()
    forecast = str(forecastobj.get_forecast(latitude= "32.7990", longitude= "-86.8073", state="florida"))
    print(forecastobj.get_forecast_description(12))

    #61.385,-152.2683
    forecastobj = dal()
    print(forecastobj.get_states())
