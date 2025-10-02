import random
from .Card import Card


class Deck(object):
    numDecks = 1
    cards = []

    def shuffle(self):
        random.shuffle(self.cards)

    def setNumDecks(self,n):
        self.numDecks = n
        self.setup()

    def setup(self):
        self.cards = []
        for i in range (self.numDecks):
            for suit in ["Hearts", "Spades", "Clubs", "Diamonds"]:
                for val in range (1,14):
                    self.cards.append(Card(val,suit))
        self.shuffle()

    def __init__(self):
        self.setup()

    def pull_card(self):
        return self.cards.pop(0)

    def print(self):
        for card in self.cards:
            print(card.abrev_str())