import paho.mqtt.client as mqttClient
import time
import json
import random

'''
global variables
'''

connected = False  # Stores the connection status
BROKER_ENDPOINT = "things.ubidots.com"
PORT = 8883
MQTT_USERNAME = "BBFF-FZEcZCMX7zB8mUz6dJjJzQzmMv8w0H"  # Put here your TOKEN
MQTT_PASSWORD = ""
TOPIC = "/v1.6/devices/"
DEVICE_LABEL = "weather-station"
VARIABLE_LABEL_1 = "temperature"
VARIABLE_LABEL_2 = "humidity"

'''
Functions to process incoming and outgoing streaming
'''


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[INFO] Connected to broker")
        global connected  # Use global variable
        connected = True  # Signal connection

    else:
        print("[INFO] Error, connection failed")


def on_publish(client, userdata, result):
    print("[INFO] Published!")


def connect(mqtt_client, mqtt_username, mqtt_password, broker_endpoint, port):
    global connected

    if not connected:
        mqtt_client.username_pw_set(mqtt_username, password=mqtt_password)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish
        mqtt_client.connect(broker_endpoint, port=port)
        mqtt_client.loop_start()

        attempts = 0

        while not connected and attempts < 5:  # Waits for connection
            print("[INFO] Attempting to connect...")
            time.sleep(1)
            attempts += 1

    if not connected:
        print("[ERROR] Could not connect to broker")
        return False

    return True


def publish(mqtt_client, topic, payload):
    try:
        mqtt_client.publish(topic, payload)
    except Exception as e:
        print("[ERROR] There was an error, details: \n{}".format(e))


def main(mqtt_client):

    # Simulates sensor values
    sensor_value_1 = random.random() * 100
    sensor_value_2 = random.random() * 100

    # Builds Payload and topíc
    payload = {VARIABLE_LABEL_1: sensor_value_1,
               VARIABLE_LABEL_2: sensor_value_2
              }
    payload = json.dumps(payload)
    topic = "{}{}".format(TOPIC, DEVICE_LABEL)

    if not connected:  # Connects to the broker
        connect(mqtt_client, MQTT_USERNAME, MQTT_PASSWORD,
                BROKER_ENDPOINT, PORT)

    # Publishes values
    print("[INFO] Attempting to publish payload:")
    print(payload)
    publish(mqtt_client, topic, payload)


if __name__ == '__main__':
    mqtt_client = mqttClient.Client()
    while True:
        main(mqtt_client)
        time.sleep(1)