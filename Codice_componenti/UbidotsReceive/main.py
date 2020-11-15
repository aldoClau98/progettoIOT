# UbidotsReceive
# Created at 2020-05-14 17:50:50.162597

import streams
import json
import requests
from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver
from servo import servo


def open(servo):
    #if(servo.getCurrentDegree()==0):
    print("Opening")
    servo.moveToDegree(180)
#    else:
#        print("Closing")
#       servo.moveToDegree(0)

def close(servo):
    print("Closing")
    servo.moveToDegree(0)

#Ubidots parameters
device_label="esp32"
variable_label="control"
token="BBFF-FZEcZCMX7zB8mUz6dJjJzQzmMv8w0H"

streams.serial()

#Servomotor Marrone -> GND Rosso -> 5V  Arancione --> D25
MyServo=servo.Servo(D22.PWM, min_width=1000, max_width=2000, default_width=1000)
MyServo.attach()

wifi_driver.auto_init()

print("Establishing connection..")
try:
    wifi.link("Vodafone-26184725", wifi.WIFI_WPA, "kfmu9axt2m9udca")
    print("Connected")
except Exception as e:
    print("Something went wrong.. ", e)
    while True:
        sleep(1000)
        
#Sending HTTP GET request to Ubidots
def get_value(device_label, variable_label, token):
    #Ubidots API Access
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + device_label + "/" + variable_label + "/lv?token=" + token
    # sends the request
    response = requests.get(url)
    # verify the status of the request
    if response.status != 200:
        return None

    print("---------------------------------")
    print("Http Status:",response.status)
    # return the last value obtained
    return response.content

while True:
    # getting last value from Ubidots
    last_value = get_value(device_label, variable_label, token)
    # verify if the last value received is not 'None'
    if last_value is not None:
        last_value  = float(last_value) * 1.0
        # Var control
        if last_value >= 1.0:
            print("Open")
            open(MyServo)  # open motor
        else:
            print("Close")
            close(MyServo)#close motor
    sleep(1500) # minimum time sleep allowed

