# -*- coding: utf-8 -*-
import socket,json
HOST = '192.168.0.1'
PORT = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
data = []
while True:
    conn, addr = server.accept()
    serverMsg = 'Connect seccess'
    conn.sendall(serverMsg.encode())
    while True:
        try:
            clientMsg = conn.recv(4096)
            serverMsg = 'hello!'
        except:
            print('\nClient disconnect!')
            break
        try:
            data = eval(clientMsg.decode())
            print('\rFrom client:', data,type(data),end='')
        except:
            continue
        
        conn.sendall(serverMsg.encode())
        
    conn.close()
