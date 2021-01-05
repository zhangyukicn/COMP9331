#python 3.7
from socket import *
import sys
import os
serverPort = int(sys.argv[1])
localhost = 'localhost'

#TCP
add= (localhost, serverPort)
serverSocket = socket(AF_INET, SOCK_STREAM)
#serverSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
serverSocket.bind(add)

serverSocket.listen(1)

while True:
    connectionSocket, address = serverSocket.accept()
    #print(connection)
    requested_file = connectionSocket.recv(1024).decode().split('/n')
    if 'GET' in requested_file[0]:
        requested_file_file = requested_file[0].split(" ")[1].replace('/','')
        file =[]
        for a in os.listdir(os.curdir):
            file.append(a)
        if requested_file_file in file and requested_file_file.endswith('.html'):
            with open(requested_file_file) as f:
                content = f.read()
            connectionSocket.send('\nHTTP/1.1 200 ok\n\n'.encode())
            connectionSocket.sendall(content.encode())
            connectionSocket.close()

        elif requested_file_file in file and requested_file_file.endswith('.jpeg'):
            connectionSocket.send('\nHTTP/1.1 200 ok\n\n'.encode())
            image = open(requested_file_file,'rb')
            image_data = image.read(1024)

            while image_data:
                print(connectionSocket.send(image_data))
                image_data = image.read()
            connectionSocket.close()
        else:
            print('requested file not exist')
            connectionSocket.send('\nHTTP/1.1 404 Not refound\n\n'.encode())
            connectionSocket.close()








