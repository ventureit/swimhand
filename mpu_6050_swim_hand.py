import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import datetime
import sys
import warnings
warnings.filterwarnings("ignore", ".*GUI is implemented.*")
g_port = 'COM6'
g_baudrate = 115200
start = time.time()

class ConnectArduino:
    def __init__(self, port, baudrate):
        # # if len(sys.argv) == 3:
        # print('# Using port: ' + g_port + " and baudrate " + str(g_baudrate))
        # self.port = serial.Serial(port=g_port, baudrate=g_baudrate)
        self.port = port

    def open(self):
        self.port.open()

    def close(self):
        self.port.close()


    def send(self, msg):
        self.port.write(msg)

    def recv(self):
        return serial.Serial('COM6', 115200)
        # return self.port.readline


class SwimMonitor(object):
    # def __init(self, parent=None):
    #     self.baudrate = 115200
    #     self.port = 'COM6'
    #
    #     self.Connect_Arduino(self.port, self.baudrate)

    @staticmethod
    def redraw_figure():
        plt.gcf().canvas.flush_events()
        plt.show(block=False)
        plt.show(block=False)

    def connect_arduino_def(self):
        return serial.Serial(port=g_port, baudrate=g_baudrate)

    def seconds_elapsed(self, start_t, end_t):
        self.start_t = start_t
        self.end_t = end_t

        py_start_t = datetime.datetime.strptime(start_t, '%X') #.strftime('%H:%M:%S')
        py_end_t = datetime.datetime.strptime(start_t, '%X') #.strftime('%H:%M:%S')
        passed_t = py_end_t - py_start_t
        print(passed_t)
        return passed_t

    def integration_data(self, acc, vel, pos, t):
        self.acc = acc
        self.vel = vel
        self.pos = pos
        self.t = t
        len_acc = acc.shape[0]

        # Velocity
        for j in range(0, len(vel[0])):
            vel[t][j] = vel[t - 1][j] + acc[j] * 0.001
            if j == 0:
                dir = 'x'
            elif j == 1:
                dir = 'y'
            else:
                dir = 'z'

            # Position
        for j in range(0, len(pos[0])):
            pos[t][j] = pos[t - 1][j] + vel[t][j] * 0.001
            if j == 0:
                dir = 'x'
            elif j == 1:
                dir = 'y'
            else:
                dir = 'z'

        return pos, vel

    def update_2d_monitor(self):

        plt.ion()
        length = 10
        lowest_y_coordinate = 0
        highest_y_coordinate = 800
        x = [0]*length             #create empty variable of length of test
        y = [0]*length
        z = [0]*length
        imu_t = [0]*length
        vel = [[0] * 3 for _ in range(length)]
        pos = [[0] * 3 for _ in range(length)]

        xline, = plt.plot(x)
        yline, = plt.plot(y)
        zline, = plt.plot(z)
        # plt.ylim([lowest_y_coordinate, 10000])

        arduino = self.connect_arduino_def()

        for t in range(length):
            data = arduino.readline()
            # data = c_arduino_object.recv()
            # print(data)
            data = data.decode('utf-8') #must use data() because it is an object?
            sep = data.split()
            # print(sep)

            if np.size(sep) == 3:
                x.append(int(sep[0])) # add new value as int to current list
                y.append(int(sep[1]))
                z.append(int(sep[2]))

                # if start_t == 0:
                #     start_t = self.seconds_elapsed(sep[3], sep[3])
                #
                # imu_t.append(self.seconds_elapsed(start_t, sep[3]))
                # start_t = imu_t[-1]
                'Removes the created parameter'
                del x[0]
                del y[0]
                del z[0]
                acc = np.array([x[-1], y[-1], z[-1]])
                pos, vel = self.integration_data(acc, vel, pos, t)

            xline.set_xdata(np.arange(len(x))) #sets xdata to new list length
            yline.set_xdata(np.arange(len(x)))  # sets xdata to new list length
            zline.set_xdata(np.arange(len(x)))  # sets xdata to new list length
            xline.set_ydata(x)
            yline.set_ydata(y)
            zline.set_ydata(z)
            # return acc

            fig = plt.figure()
            fig.canvas.draw()
            # ax = fig.gca()
            # ax.plot(x, y)
            # ax.plot(pos[:][0], pos[:][1], pos[:][2])
            # plt.xlim([0, len(x)])
            self.redraw_figure()
            # print(x[-1], y[-1], z[-1])



def main():
    SwimMonitor().update_2d_monitor()
    # ConnectArduino(g_port, g_baudrate).recv()

if __name__ == "__main__":
    main()





    # arduino_binary = arduino.readline()
    # sys.stdout.write(str(arduino_binary))
    # sys.stdout.flush()
