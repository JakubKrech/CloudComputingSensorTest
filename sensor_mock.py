import datetime, threading, json
from time import sleep
from sys import argv
import paho.mqtt.client as mqtt

import sensor_data_generator as sdg

# MQTT Settings ---------------------------------------
MQTT_Broker = "3.86.177.214" #"test.mosquitto.org"   #"54.159.150.221"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic_Temperature   = "krekan/Temperature"
MQTT_Topic_Humidity      = "krekan/Humidity"
MQTT_Topic_AirPressure   = "krekan/AirPressure"
MQTT_Topic_Contamination = "krekan/Contamination"
#------------------------------------------------------

def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print("Unable to connect to MQTT Broker")
    else:
        print("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
    pass

def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

def publish_to_topic(topic, message):
    mqttc.publish(topic, message)
    print("Published: " + str(message) + " on MQTT Topic: " + str(topic))
    print("")

toggle = 0

def publish_fake_sensor_data_to_MQTT(sensor_data, parameters):  
    global toggle
    
    Data_To_Publish = {}
    Data_To_Publish["Sensor_ID"] = sensor_data[0]
    Data_To_Publish["Sensor_Name"] = sensor_data[1]
    Data_To_Publish["Latitude"] = sensor_data[2]
    Data_To_Publish["Longitude"] = sensor_data[3]
    Data_To_Publish["Date"] = (datetime.datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
    
    if toggle == 0:
        Data_To_Publish["Temperature"] = parameters[0]
        publish_to_topic(MQTT_Topic_Temperature, json.dumps(Data_To_Publish))
        toggle = 1
    elif toggle == 1:
        Data_To_Publish["Humidity"] = parameters[1]
        publish_to_topic(MQTT_Topic_Humidity, json.dumps(Data_To_Publish))
        toggle = 2
    elif toggle == 2:
        Data_To_Publish["AirPressure"] = parameters[2]
        publish_to_topic(MQTT_Topic_AirPressure, json.dumps(Data_To_Publish))
        toggle = 3
    elif toggle == 3:
        Data_To_Publish["Pm10"] = parameters[3]
        Data_To_Publish["Pm2_5"] = parameters[4]
        Data_To_Publish["Pm1"] = parameters[5]
        publish_to_topic(MQTT_Topic_Contamination, json.dumps(Data_To_Publish))
        toggle = 0

sleep_between_readings_interval = 0.5

def main():
    if len(argv) >= 5:
        latitude = argv[1]
        longitude = argv[2]
        sensor_id = argv[3]
        sensor_name = argv[4]
    else:
        latitude = 50.067113068872125
        longitude = 19.916977590543684
        sensor_id = 0
        sensor_name = "AGH B5"

    sensor_data = [sensor_id, sensor_name, latitude, longitude]
    sensor_parameters = sdg.initialize_parameters()

    print("Sensor #{} \"{}\" started! \nLatitude: {}\nLongitude: {}".format(sensor_id, sensor_name, latitude, longitude))

    while True:
        # print("Temperature: {:6} Humidity: {:5} Air Pressure: {:7} Pm10: {:5} Pm2.5: {:5} Pm1: {:5}    Time: {}"
        #     .format(*parameters, (datetime.datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")))

        sensor_parameters = sdg.perform_next_step_generation(sensor_parameters)
        publish_fake_sensor_data_to_MQTT(sensor_data, sensor_parameters)
        sleep(sleep_between_readings_interval)
    
main()