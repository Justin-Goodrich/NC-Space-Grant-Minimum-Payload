import smbus
import time

MMA8451_ADDR = 0x1D
CTRL_REG1 = 0x2A
OUT_X_MSB = 0x01
OUT_Y_MSB = 0x03
OUT_Z_MSB = 0x05


ACTIVE_MODE = 0x01

class Accelerometer:
    def __init__(self, address) -> None:
        self.address = address

    def get_id():
        pass

    def set_active():
        pass

    def get_acceleration():
        pass

    def get_orientation():
        pass

    def set_range():
        pass

    def get_range():
        pass

    def set_rate():
        pass

    def get_rate():
        pass

    

    