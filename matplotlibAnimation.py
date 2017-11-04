import socket
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import numpy as np

style.use('ggplot')

# Stopwatch
nw=time.time()

# Setup the figure
fig = plt.figure()
sensor_plot = fig.add_subplot(1,1,1)

# Connection
HOST = '192.168.0.11'
PORT = 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))

# print('Connection' + str(conn) + 'Address' + str(addr))
start = time.time()

def stopWatch(value):
    '''From seconds to Days;Hours:Minutes;Seconds'''

    valueD = (((value/365)/24)/60)
    Days = int (valueD)

    valueH = (valueD-Days)*365
    Hours = int(valueH)

    valueM = (valueH - Hours)*24
    Minutes = int(valueM)

    valueS = (valueM - Minutes)*60
    Seconds = int(valueS)

    return valueS

    # print(Days,";",Hours,":",Minutes,";",Seconds)


# Data Management
ts = []
xs = []
ys = []
zs = []

while 1:
    def animate(i):

        # Accept Connection
        s.listen(1)
        conn, addr = s.accept()


        data = conn.recv(1024)
        dataJSON = json.loads(data.decode('utf-8'))
        dataListXYZ = list(dataJSON[0].values())

        dataListX = dataListXYZ[0]
        dataListY = dataListXYZ[1]
        dataListZ = dataListXYZ[2]
        # for i in range(1, 100):
        end = time.time()
        ts.append(stopWatch(end-start))
        xs.append(dataListX)
        ys.append(dataListY)
        zs.append(dataListZ)
        if len(ts) > 50:
            ts.pop()
            xs.pop()
            ys.pop()
            zs.pop()
            print(ts, xs)
            # print('i %s, dataList %s' % (ts, zs))

        # Plot
        # for i in range(len(dataListXYZ)):
            # print('i: ' + str(i) + ', z: ' + str(dataList[i]))
        # sensor_plot.clear
        sensor_plot.plot(ts, xs, 'b')
        sensor_plot.plot(ts, xs,'b', ts, ys,'r', ts, zs,'g')


    # Animate
    ani = animation.FuncAnimation(fig, animate, interval=1)
    plt.show()

