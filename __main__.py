from modules.dal import dal
from modules.model import produce
import pulsar, time
from pulsar.schema import *

class main:
    def __init__(self):
        d = dal()
        self.states_list = d.get_states()
        self.p = produce()
        self.generate_forecast()


    def generate_forecast(self):

        for state_dict in self.states_list:
            self.p.get_forecast_for_tomorrow(lat=state_dict["latitude"], long=state_dict["longitude"], state=state_dict["state"])
            self.p.send_msj_user_auth("52.136.127.136:6650", "forecast", "cassandra")
            self.p.send_msj_user_auth("52.136.127.136:6650", "pulsar_messages_index", "elasticsearch")


if __name__ == '__main__':
    main()




