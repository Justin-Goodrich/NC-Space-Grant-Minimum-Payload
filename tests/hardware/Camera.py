import time
from camera.CameraController import ImageCamera

camera = ImageCamera(0)
collection_interval = 0.01
collection_time = 60


print('3')
time.sleep(1)
print('2')
time.sleep(1)
print('1')
time.sleep(1)
print('start data collection\n\n')

t = time.time()

while time.time()-t < collection_time:
    camera.capture_frame()
    time.sleep(collection_interval)

camera.image_collection(1,60,'images')
