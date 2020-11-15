# Ubidots
# Created at 2020-05-13 09:14:03.856367
from servo import servo
import streams
import json
import requests
from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver

def open():
    print("Ok, opening, actual pos: ", MyServo.getCurrentDegree())
    #if(MyServo.getCurrentDegree() == 0)
    MyServo.moveToDegree(180)
    #return

def close():
    print("Ok, closing, actual pos: ", MyServo.getCurrentDegree())
    MyServo.moveToDegree(0)


#Ubidots parameters
device_label="esp32"
variable_label="ServoMotor"
token="BBFF-FZEcZCMX7zB8mUz6dJjJzQzmMv8w0H"

streams.serial()

#Servomotor Marrone -> GND Rosso -> 5V  Arancione --> D25
MyServo=servo.Servo(D25.PWM, min_width=1000, max_width=2000, default_width=1000)
MyServo.attach()

wifi_driver.auto_init()

print("Establishing connection..")
try:
    wifi.link("Vodafone-26184725", wifi.WIFI_WPA, "kfmu9axt2m9udca")
    print("Connected!")
except Exception as e:
    print("Something went wrong.. ", e)
    while True:
        sleep(1000)

#build JSON directory
def build_json(variable, value):
    try:
        data={variable: {"value":value}}
        return data
    except Exception as e:
        print("Exception catched.. ",e)
        return None
        
#Send HTTP Post request to Ubidots
def post_var(device_label, variable_label, value, token):
    # Ubidots API access
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/" + device_label + "/?token=" + token
    # data to be sent
    data = build_json(variable_label, value)
    #send request
    response=requests.post(url, json=data)
    # prints the status and the content of the request
    print("Http Status:",response.status)
    print("Http Content:",response.content)
    print("---------------------------------")
    return response
        
while True:
    try:
        motorVal= MyServo.getCurrentDegree()
        print("Posting var to Ubidots")
        post_var(device_label, variable_label, motorVal, token)
        sleep(1000)
        open()
        sleep(200)
        motorVal= MyServo.getCurrentDegree()
        print("Posting var to Ubidots")
        post_var(device_label, variable_label, motorVal, token)
        
    except Exception as e:
        print("Something went wrong..", e)
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        