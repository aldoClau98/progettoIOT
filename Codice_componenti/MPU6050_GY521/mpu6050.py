import i2c

MPU6050_I2CADDR = 0x68

def _buildVal(msd, lsd): #From 2 8bit numbers to one 16 bit number
    print('msd: ', msd, 'lsd: ', lsd)
    val = ( msd << 8 ) + lsd
    if (val >= 0x8000):
        return -((65535 - val) +1)
    else:
        return val

class MPU6050:
    
    def __init__(self, addr=MPU6050_I2CADDR, clk=400000):
        self.portI2C=i2c.I2C(I2C0, addr) #Declared port i2c ex. I2C0 on the board connected with 0x68, the i2c address of the sensor SDA on D25 n SCL on D26, 
        try:
            self.portI2C.start()
            print('initialized')
        except Exception as e:
            print(e)
        self.setup()
    
    
    def setup(self):
        print('initialized MPU6050 ')
        self.portI2C.write([0x6B,0b10000000]) #Dev Reset
        print('MPU6050 resetted')
        self.portI2C.write([0x6B,0x00])#Wake up MPU
        print('MPU6050 ready')
        

    
    def getTemp(self):
        temp=self.portI2C.write_read(0x41, 2)
        print('RowTemph ', temp[0], 'rowtempl', temp[1])
        rowTemp=_buildVal(temp[0],temp[1])
        return ((rowTemp/340)+36.53) #As in datasheet
    
    def getGyroX(self):
        gyroX = self.portI2C.write_read(0x43, 2)
        print('rowX ', gyroX[0], gyroX[1])
        return(_buildVal(gyroX[0], gyroX[1]))
    
    def getGyroY(self):
        gyroY = self.portI2C.write_read(0x45, 2)
        return(_buildVal(gyroY[0], gyroY[1]))    
    
    def getGyroZ(self):
        gyroZ = self.portI2C.write_read(0x47, 2)
        return(_buildVal(gyroZ[0], gyroZ[1]))    
    
