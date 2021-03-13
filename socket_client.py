import socket,time

HOST = '127.0.0.1'
PORT = 8000
clientMsg = 'Hello!'
connect = False
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
    connect = True
except:
    print('Unconnect ,please retry')


while(connect):
    serverMsg= client.recv(4096)
    client.send(clientMsg.encode())
    
    try:
        print('Server:', serverMsg.decode())
    except:
        print('No msg from server')
    time.sleep(0.01)

client.close()