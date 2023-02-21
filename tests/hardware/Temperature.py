import matplotlib.pyplot as plt
import json
import time
import os
from sensor.Altimeter import Altimeter

temp_sensor = Altimeter(1)
temp_sensor.set_active()
collection_interval = 0.001
collection_time = 5
ms = 0

x = []
y = []

print('3')
time.sleep(1)
print('2')
time.sleep(1)
print('1')
time.sleep(1)
print('start data collection\n\n')

t = time.time()

while time.time()-t < collection_time:
    temp = temp_sensor.get_temperature()
    x.append(ms)
    y.append(temp)
    ms+=1
    time.sleep(collection_interval)


def prompt(directory):
    i = input()
    if i in os.listdir(directory):
        print('file exists, please enter new name')
        prompt()
    return i

outputdir = 'data'
graphdir = 'graphs'
print('collection complete, please enter filename for data saving:\ndo not include file extension')
filename = prompt(outputdir)
out_file = open(os.path.join(outputdir,filename + '.json'), 'w+')

data = {
    'x':x,
    'y':y
}

json.dump(data, out_file)
out_file.close()

print('input filename for graph image:')
graph_filename = prompt(graphdir)

plt.plot(x,y)
plt.savefig(os.path.join(graphdir,graph_filename) + '.png')

