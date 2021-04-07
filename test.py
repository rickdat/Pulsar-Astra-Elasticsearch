import pulsar

from pulsar.schema import *


class Forecast(Record):
    key = String()
    content = String()


client = pulsar.Client('pulsar://52.136.127.136:6650')
producer = client.create_producer('forecast', schema=JsonSchema(Forecast))
producer.send(Forecast(key="2021-03-31T18:21:00-04:00",
                       content="A slight chance of rain showers. Mostly cloudy, with a low around 58"))