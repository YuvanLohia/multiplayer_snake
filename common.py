import pygame,random
pygame.init()
window = pygame.display.set_mode((600,600))
run = True
snake = [50,50]
snake_body =[[50,50]]
kLEFT,kRIGHT,kUP,kDOWN = False,False,False,False
apple = pygame.image.load("assets/apple.png")
apple_x = random.randint(80,540)
apple_y = random.randint(80,540)
clock = pygame.time.Clock()
while run:  
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
        run = False
    snake_body.insert(0,list(snake))
    if snake[0]+50 > apple_x and snake[0]+50 < apple_x +50 or snake[0] < apple_x +50 and snake[0] > apple_x:
        if snake[1]+50 > apple_y and snake[1]+50 < apple_y +50 or snake[1] < apple_y +50 and snake[1] > apple_y:
            apple_x = random.randint(80,540)
            apple_y = random.randint(80,540)
        else:
            snake_body.pop()
    else:
        snake_body.pop()
    for block in snake_body[1:]:
        if snake[0] == block[0] and snake[1] == block[1]:
            run = False
    window.fill((0, 255, 0))
    pygame.draw.rect(window,(0, 102, 0),(0,0,30,600))
    pygame.draw.rect(window,(0, 102, 0),(0,0,600,30))
    pygame.draw.rect(window,(0, 102, 0),(570,0,30,600))
    pygame.draw.rect(window,(0, 102, 0),(0,570,600,30))
    
    for val in snake_body:  
        
        pygame.draw.rect(window,(255,0,0),pygame.Rect(val[0],val[1],50,50))
    window.blit(apple,(apple_x,apple_y))
    pygame.display.update()
    clock.tick(150)
    
pygame.quit() 