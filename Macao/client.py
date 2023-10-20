## Imports ##
import pygame
from pygame.locals import *
from network import Network

## Pygame initialisation ##
pygame.init()
width = 800
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')
bg = pygame.image.load('img/bg.jpg')
cardFlip = pygame.mixer.Sound('cardFlip.wav')
music = pygame.mixer.music.load('music.mp3')
font=pygame.font.SysFont('Comic Sans MS', 15)
pygame.mixer.music.play(-1)

## Classes and Functions ##
class Button:#the button class is used to transform string data received from server into buttons for visuals
    def __init__(self, filename, pos):
        self.filename = filename
        fileName = 'img/' + filename + '.png'
        self.image = pygame.image.load(fileName)
        self.pos = pos

    def collidePoint(self, point):
        return self.image.get_rect().move(self.pos).collidepoint(point)#used to make them clickable

    def blit(self, display):
        display.blit(self.image, self.pos)


back = Button('back', (490, 70))
validate=Button('validate',(150,100))

def newWindow():#creates new window once the game ended
    save=this_
    winner=save[1]
    player=save[2]
    #print('usable ',winner, 'player ', player)
    pygame.init()
    width = 800
    height = 600
    display = pygame.display.set_mode((width, height))
    font=pygame.font.SysFont('Comic Sans MS', 50)
    font2=pygame.font.SysFont('Comic Sans MS', 20)
    pygame.display.set_caption('Client')
    while True:#displays correct message for each player and allows them to exit 
        display.fill((100, 100,200))

        if winner==player:
            message=font.render('Congratulations! You won!', False, (255,255,255))
            display.blit(message , (10,50))
            message2=font2.render('Press x to exit', False, (255,255,255))
            display.blit(message2 , (200,200))
        else:
            message=font.render('You lost!', False, (255,255,255))
            display.blit(message , (10,50))
            message2=font2.render('Press X to exit', False, (255,255,255))
            display.blit(message2 , (200,200))
        for event in pygame.event.get():#pygame usual quit system
                if event.type == pygame.QUIT:
                    pygame.quit()
        redrawWindow()
        

def redrawWindow():
    pygame.display.update()

def ifNotPlayer(p,n):
    if not p:
        n.send(['Empty'])
        winner=n.receive()
        return winner

def main():
    sendable=[]#stores player number and gameId and winner number
    run = True
    n = Network()
    p = int(n.getP())
    sendable.append(p)
    you_are_player_p=font.render('You are player: '+str(p), False, (255,255,255))
    no = n.receive()
    noplayer=no[0]
    sendable.append(no[1])
    cardDown = Button(str(noplayer), (350, 70))#receiving and creating a card down card
    n.send(['Send hand'])
    player = n.receive()#the initial hand received from the server
    x = -48#these x and y variables are used for card display
    y = 260
    ButtonList = []#creates a button list after the player hand list
    emptySpace=[]#this list keep record of the space left behind after a card was discarded so it can be reused
    stack = []#this stores the discarded cards
    stack.append(cardDown)
    for i in range(5):#creating a list of buttons with the player hand
        filename = player[i]
        x += 100
        ButtonList.append(Button(filename, (int(x), int(y))))
    while run:
        token=0
        n.send(['Updates'])#continuosly waiting for updates from the server
        card=n.receive()
        if card[0]== False:#this if identifies if there was a winner and ends the connection with the server
            #print('player ', card[1], ' won')
            sendable.append(card[1])
            run=False
        if len(card)>2:#since the initial updates list has 2 variables to start with, when there are more than a true update(ie a card) made a change in the game
            noplayer=card[-1][0]#once a change was made, it means a new card was discarded, it replaces the already existent card down
            cardDown = Button(str(noplayer), (350, 70))
            card_Down=font.render('Card Down:'+str(card[-1][0]), False, (255,255,255))
        else:
            card_Down=font.render('Card Down:', False, (255,255,255))
        n.send(['Display information'])
        list=n.receive()#list with number of cards left in deck and opponents cards in hand
        #print('received from Display information: ', list)
        cards_in_deck=font.render('Cards in deck:'+str(list[0]), False, (255,255,255))
        opponents=font.render('Opponents:'+str(list[1]), False, (255,255,255))
        ## Blitting ##
        display.blit(bg, [0, 0])
        back.blit(display)
        validate.blit(display)
        cardDown.blit(display)
        display.blit(you_are_player_p, (610,10))
        display.blit(cards_in_deck, (610,35))
        display.blit(opponents, (610,60))
        display.blit(card_Down, (610,110))
        for each in ButtonList:
            each.blit(display)   
        n.send(['Turn'])#the variable responsible for the player turn
        turn=n.receive()
        if turn==p:#allows the player to make a move only if it's their turn
            whose_turn=font.render('Turn: Yours', False, (255,255,255))
            display.blit(whose_turn, (610,85))
            if len(card)>2:
                if len(card[-1])==4:
                    #print('~~~~~~THIS IS THE SPECIAL CARD~~~~~', card[-1][0])#if there are updates to the game and the last one is a special card
                    if card[-1][3]==turn:# if the turn of the player is the same as the value representing the player who has to deal with the special card it will display the command
                        token=1
                        command1=font.render(str(card[-1][2])[:len(str(card[-1][2]))//2], False, (255,255,255))
                        display.blit(command1, (610,135))
                        command2=font.render(str(card[-1][2])[len(str(card[-1][2]))//2:], False, (255,255,255))
                        display.blit(command2, (610,160))
            for event in pygame.event.get():#pygame usual quit system
                if event.type == pygame.QUIT:
                    run = False
                listCopy = ButtonList.copy()#copies the button list to use instead of the original to avoid lenght errors with the for loop
                for k in range(len(ButtonList)):
                    if listCopy[k].collidePoint(pygame.mouse.get_pos()):
                         if event.type == MOUSEBUTTONDOWN:
                            value0=str(noplayer).split(' ')[0]#separates the card value from the suit to allow the correct format of how cards can be discarded
                            suit0=str(noplayer).split(' ')[2]
                            value=str(player[k]).split(' ')[0]
                            suit=str(player[k]).split(' ')[2]
                            if token==1:
                                #print('token is one')
                                if ((int(value0)==3 or int(value0)==2)and int(value) in [2,3,7]) or (int(value0)==4 and int(value) in [4,7]):
                                        emptySpace.append(ButtonList[k].pos)
                                        ButtonList[k].pos=(350,70)
                                        cardFlip.play()
                                        stack.append(ButtonList.pop(k))
                                        n.send(['Put down', [player[k], True]])
                                        noplayer=n.receive()[0]
                                        player.pop(k)
                                        winner=ifNotPlayer(player,n)
                                        x-=100
                                token=0
                            else:
                                if int(value) in [1,2,3,4,7] or value==value0 or suit==suit0:#players can only put down what is allowed
                                    emptySpace.append(ButtonList[k].pos)#once a card is discarded the list will be appended with the position to be reused
                                    ButtonList[k].pos=(350,70)
                                    cardFlip.play()
                                    stack.append(ButtonList.pop(k))
                                    if int(value) in [1,2,3,4,7]:#differentiating the special cards from the normal by using a boolean value
                                        n.send(['Put down', [player[k], True]])
                                    else:
                                        n.send(['Put down', [player[k], False]])
                                    noplayer=n.receive()[0]
                                    player.pop(k)
                                    winner=ifNotPlayer(player,n)
                                    x-=100

                if back.collidePoint(pygame.mouse.get_pos()):
                        if event.type == MOUSEBUTTONDOWN:
                            n.send(['Pick up'])
                            this=n.receive()#new card received and added to the hand
                            player.append(this)
                            #print(player)
                            filename=str(this)
                            if len(emptySpace)!=0:#if there are empty spaces left on visuals they will be reused and discarded
                                ButtonList.append(Button(filename,emptySpace[0]))
                                emptySpace.pop(0)
                                x+=100
                            else:
                                if x==652:#customising the x and y values to avoid having cards outside the borders
                                    y=420
                                    x=-48
                                    x+=100
                                    ButtonList.append(Button(filename,(int(x),int(y))))
                                else:
                                    x+=100
                                    ButtonList.append(Button(filename,(int(x),int(y))))
                if validate.collidePoint(pygame.mouse.get_pos()):#the validate button means the player ended their turn and that the next player can begin adding changes
                    if event.type == MOUSEBUTTONDOWN:
                        if turn==0:
                            turn=turn+1
                        elif turn==1:
                            turn-=1
                        n.send(['Move',turn])
                        turn=n.receive()
        else:#if it's not their turn the players can't click on buttons
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #print('not your turn')
                    font3=pygame.font.SysFont('Comic Sans MS', 40)
                    notYou=font3.render('Not your turn', False, (10,0,200))
                    display.blit(notYou , (330,220))
            whose_turn=font.render('Turn: Theirs', False, (255,255,255))
            display.blit(whose_turn, (610,85))
        redrawWindow()
    pygame.quit()
    return sendable, card[1], p
## Main ##
if __name__=='__main__':#used so if client.py is called from within another.py window it won’t be executed if imported
    try:
        this_=main()
        this_sendable=this_[0]
        #print('this is sendable: ' ,this_sendable, 'this is the other: ', this_[1], 'and this is p ', this_[2])
        newWindow()
    except:#if there is an error that doesn't allow the game to start the player will be sent to the menu page
        #print('Game ended, no server')
        pygame.quit()
