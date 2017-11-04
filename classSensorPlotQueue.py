import socket
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
from collections import deque

# Connection
HOST = '192.168.0.11'
PORT = 4444

# fig = plt.figure()
# sensor_plot = fig.add_subplot(1, 1, 1)
sensor_plot, ax = plt.subplots(1, 1, 1)
# sensor_plot.axis([0, 30, -50, 50])



# Data Management

# ts = []
# xs = []
# ys = []
# zs = []

start = time.time()

MAX_X = 250   #width of graph
MAX_Y = 70000  #height of graph

# Intialise line to horizontal line on 0
ts = deque([0.0]*MAX_X, maxlen=MAX_X)
xs = deque([0.0]*MAX_X, maxlen=MAX_X)
ys = deque([0.0]*MAX_X, maxlen=MAX_X)
zs = deque([0.0]*MAX_X, maxlen=MAX_X)

class SensorPlot:
    def __init__(self):
        # self.HOST = HOST
        # self.PORT = PORT


        # Setup the figure

        style.use('fivethirtyeight')

    def initConnection(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))

        # Accept Connection
        s.listen(1)
        conn, addr = s.accept()
        data = conn.recv(1024)

        # print('Connection' + str(conn) + 'Address' + str(addr))
        return data

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


    def update(self, ts, xs, ys, zs, start):

        # g = SensorPlot()
        data = self.initConnection()
        dataJSON = json.loads(data.decode('utf-8'))
        dataListXYZ = list(dataJSON[0].values())

        # Calculate current time from start
        end = time.time()
        ts.append(end - start)

        # Extract x, y, z from the list
        dataListX = dataListXYZ[0]
        dataListY = dataListXYZ[1]
        dataListZ = dataListXYZ[2]

        # Append x, y, z to new list
        xs.append(dataListX)
        ys.append(dataListY)
        zs.append(dataListZ)

        ts.pop(0)
        xs.pop(0)
        ys.pop(0)
        zs.pop(0)
        # print(start)
        # print(end - start)
        print(ts, xs, ys, zs)
            # print('i %s, dataList %s' % (ts, zs))
        # return ts, xs, ys, zs


def animate(self):

    # Animate
    u = SensorPlot()
    u.update(ts, xs, ys, zs, start)

    # Actually plot
    line1 = sensor_plot.plot(ts, xs, 'r', ts, ys, 'g', ts, zs, 'b')
    # print('listening data on port %s...' % PORT)

if __name__ == "__main__":
    #Animate
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
