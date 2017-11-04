import socket
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle

#Setup the figure
fig = plt.figure()
sensor_plot = fig.add_subplot(1,1,1)
ax = plt.axes(xlim=(0, 100), ylim=(0, 200))
ax.set_xlim(left=0)

z = []

#Connection
HOST = '192.168.0.11'
PORT = 4444
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))


while 1:
    #Listen for incoming messages
    s.listen(1)
    conn, addr = s.accept()
    print('Connection' + str(conn) + 'Address' + str(addr))

    # def animate(i):
    tmp = conn.recv(1024)
    dataJSON = json.loads(tmp.decode('utf-8'))
    dataList = list(dataJSON[0].values())

    # print(dataList)
    for i in range(len(dataList)):
    # print('i: ' + str(i) + ', z: ' + str(dataList[i]))
    sensor_plot.plot(i+1, dataList)
    plt.show()

ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()

