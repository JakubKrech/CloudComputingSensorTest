import json
import paho.mqtt.client as mqtt
from pymongo import MongoClient

# MQTT Settings ---------------------------------------
MQTT_Broker = "3.86.177.214" #"test.mosquitto.org" #"54.159.150.221" 
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic               = "krekan/#"
MQTT_Topic_Temperature   = "krekan/Temperature"
MQTT_Topic_Humidity      = "krekan/Humidity"
MQTT_Topic_AirPressure   = "krekan/AirPressure"
MQTT_Topic_Contamination = "krekan/Contamination"
# DB Settings -----------------------------------------
temp_data =[]
humidity_data = []
airPressure_data = []
contamination_data = []
database_batch_size = 10
client = MongoClient("mongodb+srv://kkite:kkite@mydbcloud.eu9qs.mongodb.net/<dbname>?retryWrites=true&w=majority")
mydatabase = client['KreKan']
collection=mydatabase['conditionsData']
# -----------------------------------------------------

# Subscribe to all sensors on base topic
def on_connect(mosq, obj, rc, properties=None):
    print("Subscribing to {}".format(MQTT_Topic))
    mqttc.subscribe(MQTT_Topic, 0)

# Save data into DB table !!!TO DO!!!!
def on_message(mosq, obj, msg):
    print("MQTT Data Received...")
    print("MQTT Topic: " + str(msg.topic))
    print("Data: " + str(msg.payload))

    # Save data to db
    handle_database(msg.topic, msg.payload)

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed succesfully!")
    pass

def handle_database(topic, payload):
    if(topic == MQTT_Topic_Temperature):
        temp_data.append(json.loads(payload))
        
        if(len(temp_data) == database_batch_size):
            print("Sending batch of data to database, topic: {}". format(topic))
            collection.insert_many(temp_data)
            temp_data.clear()

    if(topic == MQTT_Topic_Humidity):
        humidity_data.append(json.loads(payload))

        if(len(humidity_data) == database_batch_size):
            print("Sending batch of data to database, topic: {}". format(topic))
            collection.insert_many(humidity_data)
            humidity_data.clear()

    if(topic == MQTT_Topic_AirPressure):
        airPressure_data.append(json.loads(payload))

        if(len(airPressure_data) == database_batch_size):
            print("Sending batch of data to database, topic: {}". format(topic))
            collection.insert_many(airPressure_data)
            airPressure_data.clear()

    if(topic == MQTT_Topic_Contamination):
        contamination_data.append(json.loads(payload))

        if(len(contamination_data) == database_batch_size):
            print("Sending batch of data to database, topic: {}". format(topic))
            collection.insert_many(contamination_data)
            contamination_data.clear()

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect
mqttc.connect(MQTT_Broker, MQTT_Port, Keep_Alive_Interval)

# Continue network loop
mqttc.loop_forever()