## Imports ##

import socket, datetime
from _thread import *
import pickle
from game import Game
from classes import Deck, Player

## Socket initialisation ##
server = '127.0.0.1'
#print('Server:',server)
port=5555
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print('Server started!')

## Variable initialisation and creation ##
deck=Deck()
deck.shuffle()#after deck creation it is shuffled to make the cards be in a random order
noplayer=Player('CardDown')#noplayer is the card down needed by both clients for the game mechanics
noplayer.draw(deck)
cardDown=noplayer.hand[0]
#print('Was the card down', cardDown)
playerOne=Player('Player1')#creating player one and assigning them an initial set of cards same process applied to the other player
handOne=[]#a list created to mimic the player hand which is a list of objects to make it easier for client-server communication
for j in range(5):
        playerOne.draw(deck)
        handOne.append(str(playerOne.hand[j]))
playerTwo=Player('Player2')
handTwo=[]
for j in range(5):
        playerTwo.draw(deck)
        handTwo.append(str(playerTwo.hand[j]))

games = {}#dictionary for the games connected within the server
idCount = 0
connections=[]#list of all the connections in the server
updates=[True,0]#updates list holding the Boolean value for while game is in progress and 0 for who is the winner
turn=0#initial player value for the turn

## Functions ##
def IdUnique():#uses the time and the game index from the list to create an unique Id for the game
    DateTime=str(receivedat)
    firstSplit=DateTime.split(' ')
    secondSplit=firstSplit[0].split('-')
    secondSplit=''.join(secondSplit)
    thirdSplit=firstSplit[1].split(':')
    thirdSplit=''.join(thirdSplit)
    final=secondSplit+thirdSplit+str(gameId)
    return final

def checkHand(data,player_hand):#method used to identify and prepare the appropriate message to be sent towards the player in accordance with the rules of the game
    list=[]
    ##if a player puts down a special card, a boolean value as true will be sent and once received the server will check if the other player can deal with it or not and send the command with what the player must execute
    if data[1] == True:
       #print('this is the other players hand',player_hand)           
       for each in player_hand:
            list.append(int(each.split(' ')[0]))#creating a list with all the values of the cards in a player's hand
       #print(list)
       if str(data[0].split(' ')[0])=='4':
           if 4 in list or 7 in list:
               #print('this is a special card '+ str(data[0].split(' ')[0]))
               data.append('you must put down a 4 or a 7')
           else:
                data.append('skip your turn, you have no available moves')
       if str(data[0].split(' ')[0])=='3':
           if 2 in list or 7 in list or 3 in list:
               #print('this is a special card '+ str(data[0].split(' ')[0]))
               data.append('you must put down a 3 or a 2 or a 7')
           else:
                data.append('pick up how many cards the cardDown shows')
       if str(data[0].split(' ')[0])=='2':
           if 3 in list or 7 in list or 2 in list:
               #print('this is a special card '+ str(data[0].split(' ')[0]))
               data.append('you must put down a 3 or a 2 or a 7')   
           else:
               data.append('pick up how many cards the cardDown shows')


def threaded_client(conn, p, gameId ):#p is the value sent by the network identifying the player number
    global idCount
    global turn#use of global to keep turn and idCount the same for both players
    #print('this is valueToSend: ',int(valueToSend))#gameId Created
    test=[cardDown, int(valueToSend)]
    conn.send(pickle.dumps(str(p)))
    #print('sent ', str(p))
    conn.send(pickle.dumps(test))
    #print('sent ', cardDown)
    
    while True:#continuously waiting for information from the clients and sending responses based on information received
        try:
            data=pickle.loads(conn.recv(2048))
            if data[0]=='Send hand' and p==0:#Send hand is an initial command sent by the clients to receive their set of cards
                #print('Received: ',data)
                #print('Sent: ',handOne)
                conn.send(pickle.dumps(handOne))
            if data[0]=='Send hand' and p==1:
                #print('Received: ',data)
                #print('Sent: ',handTwo)
                conn.send(pickle.dumps(handTwo))
            if data[0]=='Pick up'and p==0:#pick up allows the players to request a card and add in their hand, action is performed for both the objects list and the strings
                playerOne.draw(deck)
                handOne.append(str(playerOne.hand[-1]))
                conn.send(pickle.dumps(str(playerOne.hand[-1])))
                #print('Received: ',data)
                #print('Sent: ',playerOne.hand[-1])
                deck.count()
            if data[0]=='Pick up'and p==1:
                playerTwo.draw(deck)
                handTwo.append(str(playerTwo.hand[-1]))
                conn.send(pickle.dumps(str(playerTwo.hand[-1])))
                #print('Received: ',data)
                #print('Sent: ',playerTwo.hand[-1])
                deck.count()
            if data[0]=='Put down':#Put down is the method allowing players to put down a card so that both connecctions can 'react' to it
                #print('Received: ',data)
                if data[1][0] in handOne:
                    index=handOne.index(data[1][0])
                    handOne.pop(index)
                    playerOne.discard(index)
                    checkHand(data[1], handTwo)#modifies the data send in updates only for special cards
                    data[1].append(1)
                elif data[1][0] in handTwo:
                    index=handTwo.index(data[1][0])
                    handTwo.pop(index)
                    playerTwo.discard(index)
                    checkHand(data[1], handOne)
                    data[1].append(0)
                conn.send(pickle.dumps(data[1]))
                updates.append(data[1])
                #print('Sent: ',data[1])
            if data[0]=='Updates':#constantly sends updates back and forth between players and server
                #print('Received: ',data)
                #print('Sent: ',updates)
                conn.send(pickle.dumps(updates))
            if data[0]=='Empty' and p==0:#Empty represents the fact that a player has no more cards in hand which makes them a winner
                #print('Received: ',data)
                #print('Sent: winner',p)
                conn.send(pickle.dumps(p))
                updates[0]=False#this being set to False will close both connections
                updates[1]=p#Overwrites the winner with the actual winner value
            if data[0]=='Empty' and p==1:
                #print('Received: ',data)
                #print('Sent: winner',p)
                conn.send(pickle.dumps(p))
                updates[0]=False
                updates[1]=p
            if data[0]=='Turn':# this just contantly reminds the players whose turn it is
                #print('Received: ',data)
                #print('Sent:',turn)
                conn.send(pickle.dumps(turn))
            if data[0]=='Move':#this is sent after the turn was changed
                #print('Received:   ',data)
                turn=data[1]
                #print('Sent:',turn)
                conn.send(pickle.dumps(turn))
            if data[0]=='Display information' and p==0:#this is used so the player can keep track of all the information needed on the screen, and in case of errors with the visuals it helps with game progress
                #print('Received:   ',data)
                conn.send(pickle.dumps([deck.count(),len(handTwo)]))
                #print('Sent:',[deck.count(),len(handTwo)])
            if data[0]=='Display information' and p==1:
                #print('Received:   ',data)
                conn.send(pickle.dumps([deck.count(),len(handOne)]))
                #print('Sent:',[deck.count(),len(handOne)])
                
        except:
            break
    print("Lost connection")
    try:
        #once a player disconnected the game will leave the games list to free space for a new game
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


## Main Loop ##
while True:
    conn, addr=s.accept()
    #print('connected to:', addr)
    connections.append(conn)
    #print('this is connections : ', addr)#keeps track of the local addresses connected
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2#using even and odd number 
    if idCount % 2 == 1:#process used to create a new game once 2 players joined
        games[gameId] = Game(gameId)
        receivedat=datetime.datetime.now().replace(microsecond=0)
        print("Creating a new game", gameId)
        valueToSend=IdUnique()
    else:
        games[gameId].ready = True
        p = 1
    
    start_new_thread(threaded_client,(conn,p, gameId))



