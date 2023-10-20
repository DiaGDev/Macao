## Imports ##
import socket
import pickle


class Network:#this class effectuates the connection between a server and its clients
    def __init__(self):
        self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server='127.0.0.1'
        self.port=5555
        self.addr=(self.server,self.port)
        self.p=self.connect()

    def getP(self):#gets the player number(ie 0 or 1)
        return self.p
    
    def connect(self):#establishing the connection
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def receive(self):#receiving function
        string=pickle.loads( self.client.recv(2048))
        #print(string)
        return string

    def send(self, data):#sending function
            try:
                self.client.send(pickle.dumps(data))
            except socket.error as e:
                print(e)

