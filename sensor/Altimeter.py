import smbus 
import time

MPL3115A2_ADDR = 0X60
STATUS = 0x00
OUT_P_MSB = 0x01
OUT_P_CSB = 0x02
OUT_P_LSB = 0x03
OUT_T_MSB = 0x04
OUT_T_LSB = 0x05
DR_STATUS = 0x06
WHO_AM_I = 0x0C
SYSMOD = 0x11
CTRL_REG1 = 0x26
CTRL_REG2 = 0x27

MODE_ACTIVE = 0x01
MODE_ALTIMETER_OSR_128 = 0xB8
MODE_ALTIMETER = 128

ALTITUDE_DIVISOR = 65536
PRESSURE_DIVISOR = 64
TEMPERATURE_DIVISOR = 256


class Altimeter:
    def __init__(self,dev) -> None:
        self.config = 0x00
        self.bus = smbus.SMBus(dev)
        time.sleep(1)
        self.id = self.bus.read_byte_data(MPL3115A2_ADDR, WHO_AM_I)
        
    def get_id(self):
        return self.id

    def configure(self,SETTING):
        self.bus.write_byte_data(MPL3115A2_ADDR,CTRL_REG1,SETTING)
        self.config = SETTING

    def wipe(self):
        self.bus.write_byte_data(MPL3115A2_ADDR,CTRL_REG1,0x00)
    
    def set_active(self):
        self.configure(self.config|MODE_ACTIVE)

    def convert_altitude_data(self,data):
        return float((data[0]<<24)|(data[1]<<16)|(data[2]<<8))/ALTITUDE_DIVISOR

    def convert_pressure_data(self,data):
        return float((data[0]<<16)|(data[1]<<8)|(data[2]))/PRESSURE_DIVISOR

    def convert_temperature_data(self,data):
        temp = ((data[0]<<8)|data[1])
        if data[0] >= 128:
            temp-=1
            temp^=65535
            temp*=-1
            
        return temp/TEMPERATURE_DIVISOR

    def get_altitude(self):
        # checks if altitude mode is on, if off, switches back to altitude
        if not (self.config & MODE_ALTIMETER):
            self.configure(self.config | MODE_ALTIMETER)

        byte_data = []

        byte_data[0] = self.bus.read_byte_data(MPL3115A2_ADDR, OUT_P_MSB)
        byte_data[1] = self.bus.read_byte_data(MPL3115A2_ADDR, OUT_P_CSB)
        byte_data[2] = self.bus.read_byte_data(MPL3115A2_ADDR, OUT_P_LSB)
        
        return self.convert_altitude_data(byte_data)
    
    def get_barometric_pressure(self):
        # checks if altitude mode is on, if on, switches back to pressure mode
        if self.config & MODE_ALTIMETER != 0:
            self.config(self.config ^ MODE_ALTIMETER)
            time.sleep(2)
        byte_data = [0,0,0]

        byte_data[0] = self.bus.read_byte_data(MPL3115A2_ADDR, OUT_P_MSB)
        byte_data[1] = self.bus.read_byte_data(MPL3115A2_ADDR, OUT_P_CSB)
        byte_data[2] = self.bus.read_byte_data(MPL3115A2_ADDR, OUT_P_LSB)

        return self.convert_pressure_data(byte_data)

    def get_temperature(self):
        byte_data = [0,0]

        byte_data[0] = self.bus.read_byte_data(MPL3115A2_ADDR, OUT_T_MSB)
        byte_data[1] = self.bus.read_byte_data(MPL3115A2_ADDR, OUT_T_LSB)

        return self.convert_temperature_data(byte_data)

    
