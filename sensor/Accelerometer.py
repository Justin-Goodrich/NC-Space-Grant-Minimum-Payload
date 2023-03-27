import smbus
import time

MMA8451_ADDR = 0x1D
OUT_X_MSB = 0x01
OUT_X_LSB = 0x02
OUT_Y_MSB = 0x03
OUT_Y_LSB = 0x04
OUT_Z_MSB = 0x05
OUT_Z_LSB = 0x06
CTRL_REG1 = 0x2A
WHO_AM_I =0x0D
XYZ_DATA_CFG =  0x0E
RANGE_2G = 0x00
RANGE_4G = 0x01
RANGE_8G = 0x03
MODE_ACTIVE = 0x01

SENSITIVITY_2G = 4096
SENSITIVITY_4G = 2048
SENSITIVITY_8G = 1024

class Accelerometer:
    def __init__(self,dev) -> None:
        self.config = 0x00
        self.bus = smbus.SMBus(dev)
        self.g_offset = False
        self.range = '2g'
        self.sensitivity = SENSITIVITY_2G
        time.sleep(1)
        self.id = self.bus.read_byte_data(MMA8451_ADDR, WHO_AM_I)

    def set_g_offset(self,offset):
        self.g_offset = offset

    def get_id(self):
        return self.id

    def configure(self,SETTING):
        self.bus.write_byte_data(MMA8451_ADDR,CTRL_REG1,SETTING)
        self.config = SETTING

    def wipe(self):
        self.bus.write_byte_data(MMA8451_ADDR,CTRL_REG1,0x00)

    def set_active(self):
        self.configure(self.config|MODE_ACTIVE)
    
    def convert_acceleration_data(self,MSB,LSB):
        acceleration = ((MSB << 8)|LSB)>>2

        if MSB >= 128:
            acceleration -=1
            acceleration ^= 16383
            acceleration*=1
       

        return acceleration/self.sensitivity

    def get_acceleration(self):
        x_msb = self.bus.read_byte_data(MMA8451_ADDR, OUT_X_MSB)
        x_lsb = self.bus.read_byte_data(MMA8451_ADDR, OUT_X_LSB)
        y_msb = self.bus.read_byte_data(MMA8451_ADDR, OUT_Y_MSB)
        y_lsb = self.bus.read_byte_data(MMA8451_ADDR, OUT_Y_LSB)
        z_msb = self.bus.read_byte_data(MMA8451_ADDR, OUT_Z_MSB)
        z_lsb = self.bus.read_byte_data(MMA8451_ADDR, OUT_Z_LSB)

        x,y,z = self.convert_acceleration_data(x_msb,x_lsb), self.convert_acceleration_data(y_msb,y_lsb),self.convert_acceleration_data(z_msb,z_lsb)
        return x,y,z

    def get_orientation():
        pass

    def set_range(self, range):
        if range == '8g':
            self.bus.write_byte_data(MMA8451_ADDR,XYZ_DATA_CFG,RANGE_8G)
            self.range = '8g'
            self.sensitivity = SENSITIVITY_8G
        if range == '4g':
            self.bus.write_byte_data(MMA8451_ADDR,XYZ_DATA_CFG,RANGE_4G)
            self.range = '4g'
            self.sensitivity = SENSITIVITY_4G
        if range == '2g':
            self.bus.write_byte_data(MMA8451_ADDR,XYZ_DATA_CFG,RANGE_2G)
            self.range = '2g'
            self.sensitivity = SENSITIVITY_2G


    def get_range(self):
        return self.range

    # def set_rate():
    #     pass

    # def get_rate():
    #     pass

    

    