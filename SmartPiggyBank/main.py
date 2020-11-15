# SmartPiggyBank
# Created at 2020-05-25 13:56:49.602729
import streams
import pwm
from servo import servo
import i2c


# import the wifi interface
from wireless import wifi
# import MQTT library
from mqtt import mqtt
# import wifi support
from espressif.esp32net import esp32wifi as wifi_driver
# Import the Zerynth APP library
from zerynthapp import zerynthapp


streams.serial()

wifi_driver.auto_init()

#global variable
global_message=0
TAR=0   #taratura giroscopio

ALLARM= "ALLARME "+"position: "+str(TAR)
OPEN =  "APERTURA "
CLOSE = "CHIUSURA "
        

MQTT_CLIENTID ="Client-sensor"
TOPIC_USER="UNISA/IOT/user"
TOPIC_BOARD="UNISA/IOT/board"

#wifi connection 

def wifi_connect():
    print("Establishing wifi Link...")
    try:
        wifi.link("TP-LINK_5D60C9",wifi.WIFI_WPA2,"69303050")
        print("wifi Link Established")
    except Exception as e:
        print("ooops, something wrong while linking :-(", e)
        while True:
            sleep(1000)

# callback function for printing data received from MQTT messages
def print_sample(client,data):
     message = data['message']
     print("sample received: ", message.payload)

# function for publishing obj on the topic
def send_sample(client,topic, obj, qos):
    print("publishing: ", obj, " on topic", topic, "with QoS", qos)
    client.publish(str(topic), str(obj), qos)

def print_connectOK(client):
    print("connected to MQTT server ")

def print_messageREC(client, data):
    global global_message
    message = data['message']
    print("topic: ", message.topic)
    print("payload received: ", message.payload)
    global_message = int(message.payload)
   



#Servomotor Functions

#Connection to servo motor on pin pwmPin, default D23, return a connected instance of servoMotor
def servoConnect(pwmPin=D23.PWM):
    #wires => Brown:GND, Red:5V, Orange: pwmPin
    servoMotor = servo.Servo(pwmPin, min_width=1000, max_width=2000, default_width=1000)
    servoMotor.attach()
    print("Servo motor attached.")
    return servoMotor

def servoOpen(servoInitialized):
   servoInitialized.moveToDegree(180)
   
def servoClose(servoInitialized):
    servoInitialized.moveToDegree(60)


#Buzzer Function, buzzer connected on pinBuzzer, default D22
def buzzerTrigger(pinBuzzer=D22.PWM, frequency=2000):
    print("Buzzer ON")
    pinMode(pinBuzzer, OUTPUT)
    period=1000000//frequency
    duty=period//2
    pwm.write(pinBuzzer, period, duty, MICROS)
    sleep(1000)
    pwm.write(pinBuzzer,0,0,0)


#Led Functions
def ledAttach(ledPin=D5):
    pinMode(ledPin, OUTPUT)
    
def ledOn(ledPin=D5):
    digitalWrite(ledPin, HIGH)
    
def ledOff(ledPin=D5):
    digitalWrite(ledPin, LOW)


#MPU6050 Functions
#MPU6050 connected on i2cPort, default I2C0 on the board (SDA on D25, SCL on D26, V in 3.3v)
#Return initialized i2c port for communication with device
def mpu6050Init(i2cPort=I2C0):
    mpuPort=i2c.I2C(i2cPort, 0x68)
    try:
        mpuPort.start()
        print("Mpu initialized")
        mpuPort.write([0x6B, 0x80]) #dev reset
        print("Mpu resetted")
        mpuPort.write([0x6B, 0x00]) #wakes up mpu
        print("Mpu init done")
        return mpuPort
    except PeripheralError as e:
        print(e)

def buildVal(msd, lsd): #From 2 8bit numbers to one 16 bit number
    val = ( msd << 8 ) + lsd
    if (val >= 0x8000):
        return -((65535 - val) +1)
    else:
        return val

#Read temperature from MPU6050 and return it , need an initialized i2c port for communication with device
def mpu6050GetTemp(initializedI2CPort): 
    temp=initializedI2CPort.write_read(0x41, 2)
    print('RowTemph ', temp[0], 'rowtempl', temp[1])
    rowTemp=buildVal(temp[0],temp[1])
    return ((rowTemp/340)+36.53) #As in datasheet
    
#Read gyroscope values from MPU6050 and return an array containing x, y and z values on indexes 0, 1 and 2. need an initialized i2c port for communication with device
def mpu6050GetGyroValues(initializedI2CPort):
    x=initializedI2CPort.write_read(0x43,2)
    y=initializedI2CPort.write_read(0x45,2)
    z=initializedI2CPort.write_read(0x47,2)
    return [buildVal(x[0],x[1]), buildVal(y[0],y[1]), buildVal(z[0],z[1])]


sleep(1000)
print("STARTING...")
        
#Main Function
try:
    # Device UID and TOKEN can be created in the ADM panel
    zapp = zerynthapp.ZerynthApp("p4ZSd_21TIyMjpQE3E5P9g", "QP1MfuJzS6qhh40QI59AMQ", log=True)
    # Start the Zerynth app instance!
    zapp.run()
    #connection wifi/mosquito
    wifi_connect()
    #create instance for MQTT connection
    client = mqtt.Client(MQTT_CLIENTID,True)
    # and try to connect to "test.mosquitto.org"
    for retry in range(5):
        try:
            client.connect("broker.mqtt-dashboard.com", 60, aconnect_cb=print_connectOK)
            break
        except Exception as e:
            print(e)
            print("re-connecting...", retry)
        if retry>=5:
            print('imposible to connect mqtt server')
            while True:
                sleep(1000)
    
    # register call back functions on publish event
    client.on(mqtt.PUBLISH, print_sample)
    #iscrizione al topic  Application
    client.subscribe([[TOPIC_BOARD, 0]])
    # start the mqtt loop
    client.loop(print_messageREC)

#connection to components
 
    servoConnected = servoConnect()
    ledAttach()
    port=mpu6050Init()

    while True:
        sleep(3000)
        #send state about smart piggyBank
        

        gyroVal=mpu6050GetGyroValues(port)
        status=" Temperature: "+str(mpu6050GetTemp(port))+"\n Gyroscope values:\n x "+str(gyroVal[0])+"\n y: "+str(gyroVal[1])+"\n z:"+str(gyroVal[2])
        print(status)
        zapp.event({"data":status})
       
         #alarm function

        if gyroVal[0]>TAR:
            buzzerTrigger()
            print(ALLARM)
            send_sample(client,TOPIC_USER,ALLARM,0)
            # send mobile notification
            zapp.notify("ALARM!","La scatola è stata capovolta")
      
        #piggyBank open
        if(global_message==1):
            print(OPEN)
            ledOn()
            servoOpen(servoConnected)
            send_sample(client,TOPIC_USER,OPEN,0)
            
            #piggyBank close
        if(global_message==2):
            print(CLOSE)
            servoClose(servoConnected)
            ledOff()
            send_sample(client,TOPIC_USER,CLOSE,0)
                
            #get state 
        if(global_message==3):
                send_sample(client,TOPIC_USER,status,0)
        global_message=0
except Exception as e:
        print("Error2: ",e)