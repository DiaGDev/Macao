## Imports ##
import random


## Classes ##
class Card(object):#card class in charge of creating the format of a card
    def __init__(self, suit, val):
        self.suit=suit
        self.value=val

    def show(self):
        print("{} of {}".format(self.value, self.suit))

    def __repr__(self):# function used to allow use of format instead of card object
        return "{} of {}".format(self.value, self.suit)
      
class Deck(object):# class used to imply actual functionality of a card
    def __init__(self):
        self.cards=[]# storing all cards in a normal deck
        self.build()

    def build(self):# uses card class to create an object for each value in 4 suits
        for s in ['Spades', 'Clubs', 'Diamonds', 'Hearts']:
            for v in range(1, 14):
                self.cards.append(Card(s,v))           

    def show(self):# display
        for c in self.cards:
            c.show()

    def shuffle(self):# uses random to mix the order of the cards in deck
        for i in range(len(self.cards)-1,0,-1):
            r=random.randint(0,i)
            self.cards[i], self.cards[r]=self.cards[r],self.cards[i]
            
    def draw(self):# removes a card picked up from the deck
        return self.cards.pop()

    def count(self):# displays and counts the amount of usable cards that are still in the deck
        #print(len(self.cards))
        return len(self.cards)
        
class Player(object):# allows player to manage cards
    def __init__(self, name):
        self.name=name
        self.hand=[]#stores cards that a player can use

    def draw(self, deck):# uses class Deck to add new cards to the hand
        self.hand.append(deck.draw())
        return self

    def showHand(self):
        for card in self.hand:
            card.show()
        
    def discard(self, k):
        return self.hand.pop(k)
