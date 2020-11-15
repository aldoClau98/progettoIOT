# MPU6050_GY521
# Created at 2020-05-09 13:38:11.108830

import streams
import i2c

streams.serial()

def init():
    global portI2C
    portI2C=i2c.I2C(I2C0, 0x68) #Declared port I2C0 on the board connected with 0x68, the i2c address of the sensor SDA on D25 n SCL on D26, 
    try:
        portI2C.start()
        print('initialized')
        portI2C.write([0x6B,0b10000000]) #dev reset
        print('dev reset')
        portI2C.write([0x6B,0x00]) #Wake up MPU 
        print('done!')
        
    except PeripheralError as e:
        print(e)
    
def buildVal(msd, lsd): #From 2 8bit numbers to one 16 bit number
    print('msd: ', msd, 'lsd: ', lsd)
    val = ( msd << 8 ) + lsd
    if (val >= 0x8000):
        return -((65535 - val) +1)
    else:
        return val
    

def getTemp(port):
    temp=port.write_read(0x41, 2)
 
    print('RowTemph ', temp[0], 'rowtempl', temp[1])
    rowTemp=buildVal(temp[0],temp[1])
    return ((rowTemp/340)+36.53) #As in datasheet
    
def getGyroX(port):
    gyroX = port.write_read(0x43, 2)
    print('rowX ', gyroX[0], gyroX[1])
    return(buildVal(gyroX[0], gyroX[1]))
    
def getGyroY(port):
    gyroY = port.write_read(0x45, 2)
    return(buildVal(gyroY[0], gyroY[1]))    
    
def getGyroZ(port):
    gyroZ = port.write_read(0x47, 2)
    return(buildVal(gyroZ[0], gyroZ[1]))    
    
    
try:
    global portI2C
    init()
    
    while True:
        #read temperature
        t=getTemp(portI2C)
        print("Temperature: ", t)
        sleep(100)
        x=getGyroX(portI2C)
        print("Gyro x: ", x)
        sleep(100)
        y=getGyroY(portI2C)
        print("Gyro y: ", y)
        sleep(100)
        z=getGyroZ(portI2C)
        print("Gyro z: ", z)
        sleep(1000)

except Exception as e:
    print(e)
        
        
        
        