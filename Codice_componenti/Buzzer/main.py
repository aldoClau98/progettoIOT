# Buzzer
# Created at 2020-05-09 09:52:50.095295
#Buzzer Driven through PWM
#==========================
#This example shows how to drive a buzzer using PWM. 
#In the example a frequency ramp going from 100 Hz to 5 KHz is generated as drive.
#The frequency is converted in period to be used as input of the pwm.rite function that require period and pulse to be expressed in milli or micro seconds (measure unit can be selected as extra parameter of the pwm.write function).
#The PWM duty cycle is set to 50% driving the buzzer with a symmetric square wave. 

import streams
import pwm

#create a serial port stream with default parameters  
streams.serial()

# the pin where the buzzer is attached to
buzzerpin = D22.PWM 

pinMode(buzzerpin,OUTPUT) #set buzzerpin to output mode
frequency=100             #define a variable to hold the played tone frequency

while True:
    period=1000000//frequency #we are using MICROS so every sec is 1000000 of micros. // is the int division, pwm.write period doesn't accept floats
    print("frequency is", frequency,"Hz")
    
    #set the period of the buzzer and the duty to 50% of the period
    pwm.write(buzzerpin,period,period//2,MICROS)
        
    # increment the frequency every loop
    frequency = frequency + 20 
        
    # reset period
    if frequency >= 5000:
        frequency=100
        
    sleep(500) 