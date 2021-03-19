import pulsar, time
from .dal import dal

class produce():

    def get_forecast_for_tomorrow(self, lat: str, long: str):
        forecastobj = dal()
        forecast = str(forecastobj.get_forecast(latitude= lat, longitude= long))
        self.forecast = forecastobj.get_forecast_description(12)
        return self.forecast

    def send_msj_user_auth(self, client: str, topic: str, technology: str):
        if technology == "cassandra":
            pharsed = '{"key":'+'"'+ str(self.forecast[0]) +'"'+ "," +'"content":'+'"'+ str(self.forecast[1]) +'"}'
            client = pulsar.Client('pulsar://'+ client)
            producer = client.create_producer(topic) #change to json schema and json formatted string
            producer.send((pharsed).encode('utf-8')) 
            client.close()
            print("Sent msj:" + pharsed)



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
    produce_obj.get_forecast_for_tomorrow(lat="38.8894", long="-77.0352")
    produce_obj.send_msj_user_auth("52.136.127.136:6650", "forecast", "cassandra")
    

    #consume
    #consume_obj = consume()
    #consume_obj.consume_msj_user_auth()


