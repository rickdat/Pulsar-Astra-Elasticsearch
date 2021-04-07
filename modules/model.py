import pulsar, time
from .dal import dal
from pulsar.schema import *


class Forecast(Record):
    key = String()
    content = String()


class produce():

    def get_forecast_for_tomorrow(self, lat: str, long: str, state: str):
        forecastobj = dal()
        self.forecast = forecastobj.get_forecast_description(element=5, latitude= lat, longitude= long, state=state)
        return self.forecast

    def send_msj_user_auth(self, client: str, topic: str, technology: str):
        msj_schema = Forecast
        if technology == "cassandra":
            pharsed_key = str(self.forecast[0])
            pharsed_value = str(self.forecast[1])
            client = pulsar.Client('pulsar://'+ client)
            producer = client.create_producer(topic, schema=JsonSchema(msj_schema)) #change to json schema and json formatted string
            producer.send(Forecast(key=pharsed_key,
                                   content=pharsed_value)) 
            client.close()
            print("Sent msj:" + pharsed_key + pharsed_value)
        if technology == "elasticsearch":
            pharsed = "{"+'"'+str(self.forecast[0])+'": "'+str(self.forecast[1])+'"}'
            client = pulsar.Client('pulsar://'+ client)
            producer = client.create_producer(topic)
            producer.send((pharsed).encode('utf-8'))
            #producer.send(('{"2021-03-28T18:00:00-04:00": "A chance of rain showers. Mostly cloudy, with a low around 47. Chance of precipitation is 40%."}').encode('utf-8'))
            client.close()
            print("elastic result", pharsed)


class consume():

    def consume_msj_user_auth(self, client_address):
        client = pulsar.Client('pulsar://'+ client_address)
        consumer = client.subscribe('forecast', 'my-subscription')
        while True:
            msg = consumer.receive()
            try:
                print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
                # Acknowledge successful processing of the message
                consumer.acknowledge(msg)
            except:
                # Message failed to be processed
                consumer.negative_acknowledge(msg)



if __name__ == '__main__':
    #produce
    produce_obj = produce()
    produce_obj.get_forecast_for_tomorrow(lat="38.8894", long="-77.0352", state = "florida")
    produce_obj.send_msj_user_auth("52.136.127.136:6650", "forecast", "cassandra")
    


    #produce
    #produce_obj = produce()
    #produce_obj.get_forecast_for_tomorrow(lat="38.8894", long="-77.0352", state="florida")
    #produce_obj.send_msj_user_auth("52.136.127.136:6650", "elastcsearch-forecast", "elasticsearch", None)

    #python3 -m PulsarPOC.model