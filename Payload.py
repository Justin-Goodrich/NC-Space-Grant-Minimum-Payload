import Accelerometer

class Payload:
    def __init__(self, accelerometer_address) -> None:
        self.Accelerometer = Accelerometer(accelerometer_address)


if __name__ == "__main__":
    pass