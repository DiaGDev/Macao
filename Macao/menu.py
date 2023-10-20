## Imports ##
import pygame, sys
from pygame.locals import *
pygame.init()

## Pygame initialisation ##
win=pygame.display.set_mode((800,600))
pygame.display.set_caption('Menu')
font=pygame.font.Font('freesansbold.ttf',100)
text=font.render('Macao',True,(255,255,255))
textRect=text.get_rect()
textRect=(250,20)

class Button:#reused class used to transforma images into buttons
    def __init__(self, filename, pos):
        self.image = pygame.image.load(filename)
        self.pos = pos

    def collidePoint(self, point):
        return self.image.get_rect().move(self.pos).collidepoint(point)

    def blit(self, display):
        display.blit(self.image, self.pos)



joinButton = Button('img/join.png', (350, 200))
LoginPlayButton=Button('img/ai.png', (350, 300))
rulesButton=Button('img/rules.png', (350, 400))

while True: # main game loop
    win.fill((100,200,200))
    joinButton.blit(win)
    LoginPlayButton.blit(win)
    rulesButton.blit(win)
    win.blit(text,textRect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        if joinButton.collidePoint(pygame.mouse.get_pos()):
            if event.type==MOUSEBUTTONDOWN:
                #print ("clicked PLAY as GUEST")
                exec(open('client.py').read())# connects the player to a new game on the server
                sys.exit()
        if LoginPlayButton.collidePoint(pygame.mouse.get_pos()):
            if event.type==MOUSEBUTTONDOWN:
                #print ("clicked LOGIN and PLAY")
                exec(open('screen.py').read())#allows use of databases
                sys.exit()
        if rulesButton.collidePoint(pygame.mouse.get_pos()):
            if event.type==MOUSEBUTTONDOWN:
                #print ("clicked RULES")
                f= open('rules.txt','r')
                print(f.read())# reads the textfile used for the rules
    
                
    pygame.display.update()

