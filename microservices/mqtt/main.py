import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from datetime import datetime
import pytz

# TODO: CRIAR DOTENV PARA DADOS ABAIXO!
url = 'http://localhost:8086'
token = '1LWy6GO7ZRQy0CnzzNZTA_KUhgznI4b78xWPvFyAm17H9tYEImJ8mXYqZmvVVCWG9fXwTUDABPvmIS68kBrr8g=='
org = 'users'
bucket = 'data'

def on_message(client, userdata, message):
    # Manda pro 
    
    val = float(str(message.payload.decode("utf-8")))
    print("received message: " , val)

    with InfluxDBClient(url=url, token=token, org=org) as database:
        p = Point("Caqueiro").tag("device", "caqueiro") \
        .field(message.topic[1:], val).time(datetime.now(pytz.UTC))

        with database.write_api(write_options=SYNCHRONOUS) as write_api:
                  write_api.write(bucket=bucket, record=p)
    


client = mqtt.Client("Listener")
client.connect("localhost", 1883, 60) 

client.loop_start()
client.subscribe("/temperature")
client.subscribe("/humidity")
client.on_message=on_message 

try:
    while True:
        time.sleep(1)
  
except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
