from pickletools import pyfloat
import pygame,socket,threading,pickle
message = []
s = socket.socket()
s1 = socket.socket()
s.connect(("192.168.1.18",1234))
s1.connect(("192.168.1.18",2525))
data = pickle.loads(s1.recv(1024))
apple = data["apple"]
player = data["no_player"]
score = []
no_player = data["no_player"]
kLEFT,kRIGHT,kUP,kDOWN = False,False,False,False
colors = [(255,0,0),(0,0,255),(255,255,0),(255,0,102)]
position = [[52,52],[500,52],[500,500],[52,500]]

snake = list(position[player])
snake_body = list([position[player]])
bb = "a"
other_bodies= {}
winner = False
winner_no = 0
name_col = ["red","blue","yellow","purple"]
def reset():
    global snake,snake_body,kLEFT,kRIGHT,kUP,kDOWN,position
    snake = list(position[player])
    snake_body = list([position[player]])
    
    kLEFT,kRIGHT,kUP,kDOWN = False,False,False,False
def recv():
    global apple,snake,snake_body,no_player,winner,winner_no
    while True:
        message = pickle.loads(s1.recv(1024))
        print(message)
        if message["player_connected"]:
            print("yes")
            reset()
            
        elif message["player_disconnected"]:
            print("no")
            if message["index"] == player:
                break
            
            no_player -= 1
        elif message["winner"]:
            winner = True
            winner_no = message["index"]
        else:
            print("apple")
            apple = message["apple"]
            
        

def main():
    global apple,score,snake,snake_body,other_bodies,kLEFT,kRIGHT,kUP,kDOWN,bb
    pygame.init()
    window = pygame.display.set_mode((600,600))
    run = True
    font = pygame.font.SysFont("comicsans",40)
    nfont = pygame.font.SysFont("arial",100)
    pygame.display.set_caption("Multiplayer Snake Game")
    appleimg = pygame.image.load("assets/apple.png")
    out = False
    clock = pygame.time.Clock()
    apple_eaten = False
    while run:  
        if not winner:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                            
                            if event.key == pygame.K_LEFT:
                                
                                kLEFT,kRIGHT,kUP,kDOWN = False,False,False,False
                                kLEFT = True
                            elif event.key == pygame.K_RIGHT:
                                
                                kLEFT,kRIGHT,kUP,kDOWN = False,False,False,False
                                kRIGHT = True
                            elif event.key == pygame.K_UP:
                                
                                kLEFT,kRIGHT,kUP,kDOWN = False,False,False,False
                                kUP = True
                            elif event.key == pygame.K_DOWN:
                            
                                kLEFT,kRIGHT,kUP,kDOWN = False,False,False,False
                                kDOWN = True
                        
            
            if kLEFT:
                snake[0] -= 2
                
            elif kRIGHT:
                snake[0] += 2
                
            elif kUP:
                snake[1] -= 2
                
            elif kDOWN:
                snake[1] += 2
            
            if snake[0] < 30 or snake[0]+50 > 570 or snake[1] < 30 or snake[1]+50 > 570:
                print("yesb")
                out = True
                reset()
            snake_body.insert(0,list(snake))
            if snake[0]+50 > apple[0] and snake[0]+50 < apple[0] +50 or snake[0] < apple[0] +50 and snake[0] > apple[0]:
                if snake[1]+50 > apple[1] and snake[1]+50 < apple[1] +50 or snake[1] < apple[1] +50 and snake[1] > apple[1]:
                    apple_eaten = True
                else:
                    snake_body.pop()
            else:
                snake_body.pop()
            
            
            
            for block1 in snake_body[1:]:
                if snake[0] == block1[0] and snake[1] == block1[1]:
                    
                    out = True
                    reset()
        
            try:
                for blockma in other_bodies[:-1]:
                    if blockma["data"] != snake_body:
                        for block4 in blockma["data"]:
                        
                            
                                if snake[0] == block4[0] and snake[1] == block4[1]:
                                    
                                    out = True
                                    reset()
            except:
                pass                            
            s.send(pickle.dumps({"data":snake_body,"apple":apple_eaten,"disconnected":False,"index":player,"out":out,"winner":False}))
            out = False
            
            apple_eaten = False
            other_bodies = pickle.loads(s.recv(10240))
            try:
                score = other_bodies[-1]["score"]
            except:
                pass
            window.fill((0, 255, 0))
            pygame.draw.rect(window,(0, 102, 0),(0,0,30,600))
            pygame.draw.rect(window,(0, 102, 0),(0,0,600,30))
            pygame.draw.rect(window,(0, 102, 0),(570,0,30,600))
            pygame.draw.rect(window,(0, 102, 0),(0,570,600,30))

            for val in other_bodies[:-1]:
                for lo in val["data"]:
                    
                
                        pygame.draw.rect(window,colors[val["index"]],pygame.Rect(lo[0],lo[1],50,50))
                        text = font.render(str(score[val["index"]]),True,(255,255,255),colors[val["index"]])
                window.blit(text,(val["data"][0]))
            window.blit(appleimg,(apple[0],apple[1]))
            
            pygame.display.update()
            clock.tick(150)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            tt = nfont.render(str(name_col[winner_no] + " Wins!!"),True,(0,0,0))
            
            window.fill((0,255,0))
            window.blit(tt,(10,300))
            pygame.display.update()
    pygame.quit() 
    s.send(pickle.dumps({"apple":False,"disconnected":True}))
    s1.close()
    s.close()
t1 = threading.Thread(target=recv)

t3 = threading.Thread(target=main)
t1.start()

t3.start()