# python 3.7
import sys
from socket import *
from threading import Thread, Lock
import time
import pickle
import os


#two input error
#if input value<0 or value>255 error，give the message error
class ValueError(Exception):
    def __init__(self, message):
        self.message = message

#if input arguements are not six number rasie TypeError
class TypeError(Exception):
    def __init__(self, message):
        self.message = message


#class udpclient
class UDPClient:
    def __init__(self,address):
        self.address = address

    def ping_send_udp(self,data,):
        ping_udp = socket(AF_INET, SOCK_DGRAM)
        ping_udp.settimeout(timeout)
        #print(type(data))
        #print(pickle.dumps(data))
        ping_udp.sendto(pickle.dumps(data),self.address)   #send to server port
        ping_udp.close()

    def send(self,data):
        Thread(target=self.ping_send_udp, args=(data,), daemon=True).start() #起了一个线程，设置为后台运行，然后启动线程

#class udpserver
class UDPServer:
    def __init__(self,address):#别人发过来，他接受,recive from other send
        self.address = address

    def ping_receive_udp(self,host): #udp_server ->接受 address 是自己 address is self.
        receive_udp = socket(AF_INET, SOCK_DGRAM)
        receive_udp.bind(self.address)
        receive_udp.settimeout(60)

        while True:
            message, clientAddress = receive_udp.recvfrom(102400000)
            data= pickle.loads(message)
            #print("I'm receiving",data[0],"from server",data[1],"distance",data[2])
            if data[4] == "ping request":
                distance = data[2]
                if distance == 1:
                #if 1，1 is the second_predecessor
                    host.Second_presuccor  = data[0]
                    #print("The second_predecessor is",host.Second_presuccor)
                if distance == 2: #if 2，2 is the first_predecessor
                    host.first_presuccor =  data[0]
                    #print("The first_predecessor is",host.first_presuccor)
                new_message = [host.peer.peer_id, data[0], distance, data, 'ping response']
                print("Ping request message received from {}".format(data[0]))
                receive_udp.sendto(pickle.dumps(new_message), Peer(data[0]).transfer_IP_address)
                #print(new_message)

            elif data[4] == 'ping response':
                #print(data)
                distance = data[2]
                if distance == 1 and host.first_successor.peer_id == data[0]:
                    host.first_successor.sequence[len(host.first_successor.sequence)-1] = 1
                    #print("len=",len(host.first_successor.sequence))
                    #print("first_d=",host.first_successor.sequence)
                    #print(data)

                if distance == 2 and host.second_successor.peer_id == data[0]:

                    host.second_successor.sequence[len(host.second_successor.sequence)-1] = 1
                    #print("len=",len(host.second_successor.sequence))
                    #print("second_d=",host.second_successor.sequence)
                    #print(data)

                print("Ping response received from Peer {}".format(data[0]))#receive_udp.close()

    def receive(self,host): #udp -> 线程
        Thread(target=self.ping_receive_udp,args=(host,), daemon=True).start()

#class tcpclient
class TCPClient:
    def __init__(self,address):
        self.address = address

    def ping_send_tcp(self,data):
        ping_tcp = socket(AF_INET, SOCK_STREAM)
        ping_tcp.connect(self.address)
        ping_tcp.settimeout(sendtimeout)
        ping_tcp.send(pickle.dumps(data))
        ping_tcp.close()

    def send(self,data):
        Thread(target=self.ping_send_tcp, args=(data,), daemon=True).start()

#class tcpserver
class TCPServer:
    def __init__(self,address):
        self.address = address

    def ping_receive_tcp(self,host):
        receive_tcp = socket(AF_INET, SOCK_STREAM)
        # receiver_tcp.settimeout(1000)
        receive_tcp.bind(self.address)
        receive_tcp.listen(1)
        while True:
            connectionSocket, address = receive_tcp.accept()
            message = connectionSocket.recv(102400000)
            data= pickle.loads(message)
            #print("the data is",data)
            new_data = None
            if data[4] == 'REQUEST_LOST_PEER':
                #print("REQUEST_LOST_PEER the data is",data)
                if data[2] == 1:
                    new_data = host.first_successor.peer_id
                if data[2] == 2:
                    new_data = host.second_successor.peer_id
                new_message = [host.peer.peer_id, data[0], new_data, None,'REQUEST_LOST_PEER']
                #print("new message is",new_message)
                connectionSocket.sendall(pickle.dumps(new_message))

            elif data[4] == "QUIT":
                #print("QUIT the data is",data)
                #print(host.first_successor.peer_id , data[0])
                #print(host.second_successor.peer_id , data[0])
                if host.first_successor.peer_id == data[0]:
                    host.first_successor = host.second_successor
                    #print("no")
                    host.second_successor = Peer(data[2])
                if host.second_successor.peer_id == data[0]:
                    #print("yes")
                    host.second_successor = Peer(data[2])

                print("Peer {} will depart from the network".format(data[0]))
                print("My new first successor is Peer {}".format(host.first_successor.peer_id))
                print("My new second successor is Peer {}".format(host.second_successor.peer_id))


            elif data[4] == "Peer_Join":
                #print(data)
                join_peer =  data[0]
                #print('join_peer is ',join_peer)
                first_successor_id = host.first_successor.peer_id
                #print('first_successor_id ',first_successor_id)
                #print(type(join_peer))
               # print(type(first_successor_id))
                #print(type(host.peer.peer_id))

                if int(join_peer) < first_successor_id < host.peer.peer_id or host.peer.peer_id < int(join_peer) < first_successor_id \
                    or (first_successor_id < host.peer.peer_id and int(join_peer) > host.peer.peer_id):
                    print("Peer {} Join request received".format(join_peer))
                    #print("ok")

                    #known_peer = Peer(join_peer)
                    send_message = [host.peer.peer_id, join_peer, [host.first_successor.peer_id, host.second_successor.peer_id],None,"REQUEST_PEER_ACCEPTED"]
                    TCPClient(Peer(join_peer).transfer_IP_address).send(send_message)

                    #print("peer",type(host.peer.peer_id))
                    #print("join_peer",type(join_peer))
                    #print("Second_presuccor",type(Peer(host.Second_presuccor).peer_id))


                    receive_message = [host.peer.peer_id, Peer(host.Second_presuccor).peer_id, join_peer, None, "REQUEST_PEER_CHANGE"]
                    TCPClient(Peer(host.Second_presuccor).transfer_IP_address).send(receive_message)
                    host.first_successor = Peer(join_peer)
                    host.second_successor = Peer(first_successor_id)

                    print("My new first successor is Peer {}".format(host.first_successor.peer_id))
                    print("My new second successor is Peer {}".format(host.second_successor.peer_id))

                else:
                    message = [data[0], host.first_successor.peer_id, data[2], None, "Peer_Join"]
                    print("Peer {} Join request forwarded to my successor".format(join_peer))
                    TCPClient(host.first_successor.transfer_IP_address).send(message)
                    #print(host.first_successor)
                    #print(data)

            elif data[4] == "REQUEST_PEER_CHANGE":
                print("Successor Change request received")
                host.second_successor = Peer(data[2])
                print("My new first successor is Peer {}".format(host.first_successor.peer_id))
                print("My new second successor is Peer {}".format(host.second_successor.peer_id))


            elif data[4] == "REQUEST_PEER_ACCEPTED":
                host.first_successor =Peer(data[2][0])
                host.second_successor = Peer(data[2][1])
                print("Join request has been accepted")
                print("My new first successor is Peer {}".format(host.first_successor.peer_id))
                print("My new second successor is Peer {}".format(host.second_successor.peer_id))

            elif data[4] == "REQUEST_STORE":
                show_peer = data[3]
                find_peer_id = data[2] % cycle_number

                if (Peer(find_peer_id).peer_id == host.peer.peer_id) \
                        or(host.Second_presuccor<Peer(find_peer_id).peer_id< host.peer.peer_id) \
                            or (host.peer.peer_id < Peer(host.Second_presuccor).peer_id < Peer(find_peer_id).peer_id):
                    print("Store {} request accepted".format(data[3]))
                else:
                    #print("ok")
                    #find_peer_id = data[2] % cycle_number
                    #print(data[0],data[1],data[2])
                    print('Store {} request forwarded to my successor'.format(data[3]))
                    message = [host.peer.peer_id, host.first_successor.peer_id, find_peer_id, show_peer, "REQUEST_STORE"]
                    #print(message)
                    TCPClient(host.first_successor.transfer_IP_address).send(message)

            elif data[4] == "RESPONSE_FILE":
                filename, file_data = data[2]
                received_file = str.format("received_{}.pdf", filename)
                if os.path.exists(received_file):
                    os.remove(received_file)
                print("Peer {} had File {}".format(data[0],data[3]))
                print("Receiving File {} from Peer {}".format(data[3],data[0]))

                with open(received_file, 'ab+') as open_file:
                    open_file.write(file_data)
                print("File {} received".format(data[3]))


            #Request 4103
            elif data[4] == "REQUEST_FILE":
                show_peer = data[3]
                #data = data[2]
                peer_id, file_data = data[2]
                find_peer_id = int(data[2][1]) % cycle_number

                if (find_peer_id == host.peer.peer_id) \
                        or(host.Second_presuccor<Peer(find_peer_id).peer_id< host.peer.peer_id)\
                        or((host.peer.peer_id < Peer(host.Second_presuccor).peer_id < Peer(find_peer_id).peer_id)):
                    print("File {} is stored here".format(data[3]))
                    #print("I receive",data)
                    pdf_file_name = str(data[3]) + ".pdf"
                    #print(pdf_file_name)
                    #print("ok")
                    if os.path.exists(pdf_file_name):
                        #print("ok")

                        print("Sending file {} to Peer {}".format(data[3],data[5]))
                        #message = [host.peer.peer_id, Peer(pdf_file_name).peer_id, None,None,"RESPONSE_FILE"]
                        with open(pdf_file_name, 'rb') as open_file:
                            message = [host.peer.peer_id, Peer(peer_id).peer_id,[peer_id, open_file.read()],data[3],"RESPONSE_FILE",data[5]]
                        TCPClient(Peer(data[5]).transfer_IP_address).send(message)
                        print("The file has been sent")

                else:
                    print("Request for File {} has been received, but the file is not stored here".format(data[3]))
                    message = [host.peer.peer_id, host.first_successor.peer_id, [host.peer.peer_id,find_peer_id], show_peer, "REQUEST_FILE", data[5]]
                    #print("Request for File",message)
                    TCPClient(host.first_successor.transfer_IP_address).send(message)



        #receive_udp.close()

    def receive(self,host):
        Thread(target=self.ping_receive_tcp,args=(host,), daemon=True).start()

#class Peer,contain the point number, the point'transport port and the (IP address+ transport port)
class Peer:
    def __init__(self,peer_id):
        self.peer_id = int(peer_id)
        self.transport_port = int(self.peer_id) + base_port
        self.transfer_IP_address = (IP_address,self.transport_port)
        #self.first_presuccor = None
        #self.Second_presuccor = None

        #record_about_ peer request and response
        self.sequence =[]


class Initalization:
    def __init__(self,peer,first_successor,second_successor,ping_interver):
        if second_successor == None:
            self.peer = Peer(peer)
            self.first_successor = Peer(first_successor)
            self.second_successor = None
            self.ping_interver = ping_interver
            self.first_presuccor = None
            self.Second_presuccor = None
        else:
            self.peer = Peer(peer)
            self.first_successor = Peer(first_successor)
            self.second_successor = Peer(second_successor)
            self.ping_interver = ping_interver
            self.first_presuccor = None
            self.Second_presuccor = None

    def begin_show(self):#  step 1

        print("Start peer {} at port {}".format(peer,self.peer.transport_port))
        print("Peer {} can find first successor on port {} and second successor on port {}.".format(peer,self.first_successor.transport_port,self.second_successor.transport_port))

    def Peer_Joining(self, peer, exist_peer,ping_interver):
        #peer = self.id
        #exit_peer = self.exit_peer
        self.current_peer = Peer(peer)
        self.ping_interver = int(ping_interver)

        Host.ping_tcp_receiver()
        Host.ping_udp_receiver()

        message = [peer, exist_peer, self.current_peer.peer_id ,None,"Peer_Join"]
        #print("Peer_Joining send the message is ",message)
        TCPClient(Peer(exist_peer).transfer_IP_address).send(message)


    def ping_tcp_receiver(self):
        severaccept = TCPServer(self.peer.transfer_IP_address)
        severaccept.receive(self)

    def ping_udp_receiver(self):
        severaccept = UDPServer(self.peer.transfer_IP_address)
        severaccept.receive(self)

    def check_alive(self,current_peer,index_of_current_peer,next_peer):
        check_peer_alive = current_peer.sequence
        #print("I am peer",current_peer.peer_id,"and my sequence is",check_peer_alive)
        distance  = index_of_current_peer

        if len(check_peer_alive) <3:
            return
        else:
            if check_peer_alive[-1]==0 and check_peer_alive[-2]==0 and check_peer_alive[-3] == 0:
                print("Peer {} is no longer alive".format(current_peer.peer_id))

                tcp_sender = socket(AF_INET, SOCK_STREAM)
                tcp_sender.settimeout(sendtimeout)
                tcp_sender.connect(next_peer.transfer_IP_address)

                send_message = [self.peer.peer_id, next_peer.peer_id, distance, None, 'REQUEST_LOST_PEER']
                #print("send_message is",send_message)
                tcp_sender.send(pickle.dumps(send_message))

                receive_message = tcp_sender.recv(102400)
                data = pickle.loads(receive_message)
                #print("receive message is",data)

                if index_of_current_peer == 1:
                    self.first_successor = self.second_successor
                    self.second_successor = Peer(data[2])
                elif index_of_current_peer ==2 :
                    self.second_successor = Peer(data[2])


                print("My new first successor is Peer {}".format(self.first_successor.peer_id))
                print("My second first successor is Peer {}".format(self.second_successor.peer_id))
                tcp_sender.close()

    def ping_successor(self):
        while(True):

            #first_successor = self.first_successor
            #second_successor = self.second_successor
            if self.first_successor and self.second_successor:
                self.check_alive(self.first_successor,1,self.second_successor)
                self.check_alive(self.second_successor,2,self.first_successor)

                print("Ping requests sent to Peers {} and {}".format(self.first_successor.peer_id,self.second_successor.peer_id))

            #ping 第一个 successor 发送数据
            #self.first_successor.sequence =[]
            #current_sequence =len(self.first_successor.sequence)
                self.first_successor.sequence.append(0)
                distance =1
                data =[self.peer.peer_id, self.first_successor.peer_id, distance,self.first_successor.sequence,"ping request"]
            #print("I'm sending",data[0],"to server",data[1],"accept just",distance,"server's sequence is",data[3],"and is",data[4])
                UDPClient(self.first_successor.transfer_IP_address).send(data)


            #ping 第二个 successor 发送数据
            #current_sequence =len(self.second_successor.sequence)
                self.second_successor.sequence.append(0)
                distance = 2
                data =[self.peer.peer_id, self.second_successor.peer_id, distance,self.second_successor.sequence ,"ping request"]
            #print("I'm sending",data[0],"to server",data[1],"accept just",distance,"server's sequence is",data[3],"and is",data[4] )
                UDPClient(self.second_successor.transfer_IP_address).send(data)

                time.sleep(self.ping_interver)

    def ping_successors_thread(self):
        ping_sender_thread = Thread(target=self.ping_successor)
        ping_sender_thread.setDaemon(True)
        ping_sender_thread.start()

    def check_input(self):
        while True:
            line = sys.stdin.readline()
            if line.startswith("Quit"):
                '''
                #can't debug still wrong
                if self.first_presuccor and self.Second_presuccor:
                    data=self.first_successor.peer_id
                    message =[self.peer.peer_id, Peer(self.first_presuccor).peer_id, data, None, "QUIT"]
                    TCPClient(Peer(self.first_presuccor).transfer_IP_address).send(message)


                    data = self.second_successor.peer_id
                    message =[self.peer.peer_id, Peer(self.Second_presuccor).peer_id, data, None, "QUIT"]
                    TCPClient(Peer(self.Second_presuccor).transfer_IP_address).send(message)

                    sys.exit(0)
                '''
      
                if self.first_presuccor and self.Second_presuccor:
                    ping_tcp = socket(AF_INET, SOCK_STREAM)
                    ping_tcp.settimeout(20)

                    data=self.first_successor.peer_id
                    message =[self.peer.peer_id, Peer(self.first_presuccor).peer_id, data, None, "QUIT"]
                    #print(message)
                    ping_tcp.connect(Peer(self.first_presuccor).transfer_IP_address)
                    ping_tcp.send(pickle.dumps(message))
                    ping_tcp.close()


                    ping_tcp = socket(AF_INET, SOCK_STREAM)
                    ping_tcp.settimeout(20)
                    data = self.second_successor.peer_id
                    message =[self.peer.peer_id, Peer(self.Second_presuccor).peer_id, data, None, "QUIT"]
                    #print(message)
                    ping_tcp.connect(Peer(self.Second_presuccor).transfer_IP_address)
                    ping_tcp.send(pickle.dumps(message))
                    ping_tcp.close()

                    sys.exit(0)

            if line.startswith("Store"): #Store 2067
                number = line.split()
                if len(number) == 2 and 0 < int(number[1]) <=9999 and len(number[1]) == 4:
                    print('Store {} request forwarded to my successor'.format(int(number[1])))
                    message = [self.peer.peer_id, self.first_successor.peer_id, int(number[1]), int(number[1]), "REQUEST_STORE"]
                    TCPClient(self.first_successor.transfer_IP_address).send(message)
                else:
                    print("Store invalid filename {}".format(number[1]))

#Request 512
            if line.startswith("Request"):
                number = line.split()
                if len(number) == 2 and 0 < int(number[1]) <=9999 and len(number[1]) == 4:
                    print("File request for {} has been sent to my successor".format(int(number[1])))
                    message = [self.peer.peer_id, self.first_successor.peer_id, [self.peer.peer_id,int(number[1])], int(number[1]), "REQUEST_FILE" ,self.peer.peer_id]
                    TCPClient(self.first_successor.transfer_IP_address).send(message)
                else:
                    print("Request invalid filename {}".format(number[1]))







#define golobal variation

if __name__== '__main__':

    cycle_number = 256        # %256
    base_port = 12000         #base_port
    IP_address = '127.0.0.1'
    TYPE = sys.argv[1]
    timeout = 10
    sendtimeout = 20
    #print(TYPE)

    if TYPE == "init":
        peer = sys.argv[2]
        first_successor = int(sys.argv[3])
        #print(sys.argv[3])
        second_successor = int(sys.argv[4])
        #print(sys.argv[4])
        ping_interver = int(sys.argv[5])

        if len(sys.argv) != 6:
            raise TypeError("missing required positional argument")
        if int(sys.argv[3]) < 0 or int(sys.argv[4]) > 255:
            raise ValueError("Value is not meet the requirement")
        else:
            Host = Initalization(peer,first_successor,second_successor,ping_interver)
            Host.begin_show()
            Host.ping_udp_receiver()
            #print(Host.peer)
            Host.ping_tcp_receiver()
            Host.ping_successors_thread()
            Host.check_input()



    elif TYPE == "join":
        peer = sys.argv[2]
        exit_peer_id = sys.argv[3]
        ping_interver = sys.argv[4]
        if len(sys.argv) != 5:
            raise TypeError("missing required positional argument")
        if int(sys.argv[2]) < 0 or int(sys.argv[3]) > 255:
            raise ValueError("Value is not meet the requirement")
        else:
            Host = Initalization(peer,exit_peer_id,None,ping_interver)
            #peer_join.ping_udp_receiver()
            #peer_join.ping_tcp_receiver()

            Host.Peer_Joining(peer,exit_peer_id,ping_interver)
            #Host.ping_udp_receiver()
            #print(Host.peer)
            #Host.ping_tcp_receiver()

            Host.ping_successors_thread()

            Host.check_input()

        #Request 4103
        #Store 4103





