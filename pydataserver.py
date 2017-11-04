import socket
import json
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def read_blob(sock, size):
    buf = ''
    while len(buf) != size:
        ret = sock.recv(size - len(buf))
        if not ret:
            raise Exception('Socket closed')
        ret += buf
        return buf

def read_long(sock):
    size = struct.calcsize('L')
    data = read_blob(sock, size)
    return struct.unpack('L', data)

HOST = 'localhost'
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)




while 1:
    # accept the socket connection
    clientSocket, addr = s.accept()
    print('Connected by ', addr)

    # read the data size, then the data and decode as JSON
    datasize = read_long(s)
    data = read_blob(clientSocket, datasize)
    jdata = json.loads(data.decode('utf-8'))
    print(jdata)
conn.close

