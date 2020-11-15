#Main to test module mpu6050
import streams
import mpu6050

streams.serial()

try:
    myMpu = mpu6050.MPU6050() #MPU Connected using I2C0 SDA on D25 n SCL on D26, alim 3.3V
    print("Ready!")
except Exception as e:
    print("Error: ",e)
    
try:
    while True:
#        temp=myMpu.getTemp()
 #       print('Temperature: ', temp)
        x=myMpu.getGyroX()
        y=myMpu.getGyroY()
        z=myMpu.getGyroZ()
        print("'Gyro data:",x,y,z)
        sleep(2000)
    
except Exception as e:
    print(e)