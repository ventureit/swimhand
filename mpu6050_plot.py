import serial, re, time
import numpy as np
import matplotlib.pyplot as plt

# connect to Arduino port with 38400 baud
arduino = serial.Serial('COM6',115200)

hz = 250
interval = 1/hz

def sampling_round(value, hz):
    return round(value*hz)/hz

no_of_coordinates = 200
now = int(time.time())
past = now - (no_of_coordinates/hz) # hz is the number of samples per second, gives the right number of x-coordinates to match y-coordinates
future = now
#print('past', past)
#print('future', future)

lowest_y_coordinate = 0
highest_y_coordinate = 800

plt.ion()
accel_xdata = [0.0] * no_of_coordinates
accel_ydata = [0.0] * no_of_coordinates
accel_zdata = [0.0] * no_of_coordinates
x_axis = np.arange(past, future, interval).tolist()
# line_accel_x, = plt.plot(x_axis, accel_xdata)
# line_accel_y, = plt.plot(x_axis, accel_ydata)
# line_accel_z, = plt.plot(x_axis, accel_zdata)
# plt.ylim([lowest_y_coordinate, highest_y_coordinate])
# plt.xlim([past, future])


while True:
    data = arduino.readline()[:-2]
    data = data.decode("utf-8")
    if data and data[0] == 'X': # start from x-coordinate values
        coordinates = re.match(r'X.(\d{3}).Y.(\d{3}).Z.(\d{3})',data, re.I) # parse only values
        #print(coordinates.group(1))
        #print(coordinates.group(2))
        #print(coordinates.group(3))
        now = sampling_round(time.time(), hz)
        if x_axis[-1] != now:
            x_axis.append(now)
        else:
            continue
        accel_xdata.append(int(coordinates.group(1)))
        accel_ydata.append(int(coordinates.group(2)))
        accel_zdata.append(int(coordinates.group(3)))
        del x_axis[0]
        del accel_xdata[0]
        del accel_ydata[0]
        del accel_zdata[0]
        # line_accel_x.set_xdata(x_axis)
        # line_accel_y.set_xdata(x_axis)
        # line_accel_z.set_xdata(x_axis)
        # line_accel_x.set_ydata(accel_xdata)
        # line_accel_y.set_ydata(accel_ydata)
        # line_accel_z.set_ydata(accel_zdata)
        # plt.xlim([x_axis[0],x_axis[-1]])
        # plt.draw()
        print(x_axis[0],x_axis[-1])
    else:
        continue