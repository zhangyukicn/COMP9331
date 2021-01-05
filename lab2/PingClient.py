# python 3.7
from socket import *
from datetime import datetime
import sys



hostname = "127.0.0.1"
serverName = hostname
serverPort = int(sys.argv[2])
address = (serverName,serverPort)
clientSocket = socket(AF_INET,SOCK_DGRAM)

l_rtts = []
lost_count =0

for i in range(0,10):
    begin_time = datetime.now()
    message = "PING" + str(i) + ' ' + str(begin_time) + '\r\n'
    clientSocket.sendto(message.encode(),address)
    try:
        clientSocket.settimeout(1.0)
        clientSocket.recv(1024)
        end_time = datetime.now()
        rtts_time = int((end_time - begin_time).total_seconds()*1000)
        l_rtts.append(rtts_time)
        print("PING to {}, seq = {}, rtt ={} ms").format(serverName,str(i),rtts_time)
        clientSocket.settimeout(None)
    except timeout:
        lost_count = lost_count + 1
        print("PING to {}, seq = {}, rtt = time out").format(serverName,str(i))

print("\n")
print('Minimum RTT = {} ms'.format(min(l_rtts)))
print('Maximum RTT = {} ms'.format(min(l_rtts)))
print('Average RTT = {} ms'.format(round(float(sum(l_rtts) / len(l_rtts)))))
clientSocket.close()
