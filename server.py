import random,pickle,threading,socket
class Room:
    def __init__(self):
        self.list_clients = []
        self.list_clients1 = []
        self.no_of_players = 0
        self.index = 0
        
        self.score = []

        self.apple = (random.randrange(50,500),random.randrange(50,500))
        t = threading.Thread(target= self.handle)
        t.start()
        
    def full(self):
        if self.index==4:
            return True
        else:
            return False
    def append(self,c,c1):
        
        
        c1.send(pickle.dumps({"apple":self.apple,"no_player":self.index}))
        self.score.append(0)
        
        for kl in self.list_clients1:
            kl.send(pickle.dumps({"player_connected":True,"player_disconnected":False,"winner":False}))
        self.no_of_players += 1    
        self.index += 1
        self.list_clients.append(c)
        self.list_clients1.append(c1)    
    def disconect(self,c,c1):
        
        
        for kl in self.list_clients1:
            kl.send(pickle.dumps({"player_connected":False,"player_disconnected":True,"index":self.list_clients.index(c),"winner":False}))
        
        self.score.pop(self.list_clients.index(c))
        self.no_of_players -= 1
        self.list_clients1.remove(c1)
        self.list_clients.remove(c)
        
        c.close()
        c1.close()
    def handle(self):
        while True:
            for olol in self.score:
                if olol >= 40:
                    for kl in self.list_clients1:
                        kl.send(pickle.dumps({"player_connected":False,"player_disconnected":False,"index":self.score.index(olol),"winner":True}))
            
            if self.no_of_players == 0 and self.index != 0:
                self.index = 4
                break
            message = []
            for i in range(self.no_of_players):
                cmess = pickle.loads(self.list_clients[i].recv(10240))
                
                
                
                if cmess["disconnected"]:
                    self.disconect(self.list_clients[i],self.list_clients1[i])
                    break
                else:
                    if cmess["apple"]:
                        self.reset_apple(i)
                    if cmess["out"]:
                        self.score[i] = 0
                    message.append({"index":cmess["index"],"data":cmess["data"]})
            message.append({"score":self.score})
            for k in self.list_clients:
                
                k.send(pickle.dumps(message))
            
    def reset_apple(self,i):
        self.apple = (random.randrange(50,500),random.randrange(50,500))
        self.score[i] += 1
        for kl in self.list_clients1:
            kl.send(pickle.dumps({"apple":self.apple,"player":i,"player_connected":False,"player_disconnected":False,"winner":False}))
    
s = socket.socket()
s1 = socket.socket()
s.bind(("192.168.1.18",1234))
s1.bind(("192.168.1.18",2525))
s.listen()
s1.listen()
rooms = []
r = Room()
rooms.append(r)

def auto_run():
    while True:
        c,_ = s.accept()
        c1,_ = s1.accept()
        
        if rooms[-1].full():
            r1 = Room()
            rooms.append(r1)
        rooms[-1].append(c,c1)

main_thread = threading.Thread(target=auto_run)
main_thread.start()
        