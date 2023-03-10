import time
import sqlite3
import threading
import os
from sensor import Accelerometer, Altimeter
from camera.CameraController import ImageCamera

BASE_DIR = '~'
DB = 'minimum_payload.db'
IMAGE_BASE_FILENAME = 'min_payload_img'
DATA_COLLECTION_INCREMENT = 15
ALTITUDE_THRESHOLD_M = 20

ALTITUDE_RANGES = [
    {
    'label':'Phase 1',
    'min':0,
    'max':1000
    },
    {
    'label':'Phase 2',
    'min':1000,
    'max':5000
    },
    {
    'label':'Phase 3',
    'min':5000,
    'max':10000
    }, 
    {
    'label':'Phase 4',
    'min':5000,
    'max':10000
    }
]

t = time.time()

con = sqlite3.connect(os.path.join(BASE_DIR, DB))
db = con.cursor()

db.execute("CREATE TABLE MIN_PAYLOAD (flight_time DOUBLE PRIMARY KEY,acceleration DOUBLE NOT NULL,temperature DOUBLE NOT NULL,barometric_pressure DOUBLE NOT NULL,altitude DOUBLE NOT NULL,image_filename TEXT NOT NULL)")
altimeter = Altimeter.Altimeter(1)
accelerometer = Accelerometer.Accelerometer(1)
camera = ImageCamera(0)

altimeter.set_active()
accelerometer.set_active()
accelerometer.set_range('4g')

alt_0 = altimeter.get_altitude()


def data_collection():
    for A in ALTITUDE_RANGES:
            img_count = 0
            photo_dir = os.path.join(BASE_DIR,A['label'])
            os.mkdir(photo_dir)
            
            while altimeter.get_altitude() < A['max']:
                photo_path = os.path.join(photo_dir, 'min_payload_img_{}.jpg'.format(img_count))
                img_count+=1
                image = camera.capture_frame()
                acceleration = accelerometer.get_acceleration()
                pressure = altimeter.get_barometric_pressure()
                altitude = altimeter.get_altitude()
                temperature = altimeter.get_temperature()
                db.execute(
                    "INSERT INTO MIN_PAYLOAD VALUES({},{},{},{})"
                    .format(time.time() - t,acceleration,temperature,pressure,altitude,photo_path)
                )
                con.commit()
                camera_thread = threading.Thread(target=camera.save_image,args=(photo_path,image))
                camera_thread.start()
                time.sleep(DATA_COLLECTION_INCREMENT)



def check_freefall():
    x,y,z = accelerometer.get_acceleration()
    if (z + 1) < 0.1:
        pass
        #activate individual payload

# main loop
while True:
    # checks when to start launch sequence
    if altimeter.get_altitude() >= alt_0 + ALTITUDE_THRESHOLD_M:
        # ecxcute thees int their own threads

        data_thread = threading.Thread(target=data_collection)
        data_thread.start()
        freefall_thread = threading.Thread(target=check_freefall)
        freefall_thread.start()

        freefall_thread.join()

        """
        IMPORTANT, CAUSES THREAD TO BLOCK UNTIL PAYLOAD IS IN FREEFALL ONCE THE THREAD TERMINATES,
        THIS IF STAMENT WILL NOT BE EXECUTED AGAIN AND ASCENT SEQUENCE IS OVER
        """


    
