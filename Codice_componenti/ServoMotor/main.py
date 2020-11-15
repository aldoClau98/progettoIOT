# ServoMotor
# Created at 2020-05-09 08:57:20.394039

from servo import servo
import streams
import pwm

def open():
    print("Ok, opening, actual pos: ", MyServo.getCurrentDegree())
    #if(MyServo.getCurrentDegree() == 0)
    MyServo.moveToDegree(180)
    #return

def close():
    print("Ok, closing, actual pos: ", MyServo.getCurrentDegree())
    MyServo.moveToDegree(0)


streams.serial()

#Servomotor Marrone -> GND Rosso -> 5V  Arancione --> D23
MyServo=servo.Servo(D25.PWM, min_width=1000, max_width=2000, default_width=1000)
while True:
    print("Servo ON")
    MyServo.attach()
    sleep(3000)
    open()
    sleep(3000)
    close()
    sleep(3000)
    open()
    sleep(3000)
    close()
    sleep(3000)
    
    print("Servo OFF")
    MyServo.detach()
    sleep(30000)