import matplotlib.pyplot as plt
import json
import time
import os
from sensor.Altimeter import Altimeter

temp_sensor = Altimeter(1)
t = time.time()
collection_interval = 0.001
collection_time = 5
ms = 0

x = []
y = []

while time.time()-t < collection_time:
    temp = temp_sensor.get_temperature()
    x.append(ms)
    y.append(temp)
    ms+=1
    time.sleep(collection_interval)

def prompt():
    print('collection complete, please enter filename for data saving')
    i = input()
    if i in os.listdir(outputdir):
        print('file exists, please enter new name')
        prompt()
    return i

outputdir = 'data'
filename = prompt()
out_file = open(os.path.join(outputdir,filename), 'w+')