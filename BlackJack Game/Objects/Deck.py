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
        self.aces = self.numDecks * 4
        self.tens = self.numDecks * 4 * 4        # 4 suits * 4 ten values (10, J, Q, K)
        self.nines = self.numDecks * 4
        self.eights = self.numDecks * 4
        self.sevens = self.numDecks * 4
        self.sixes = self.numDecks * 4
        self.fives = self.numDecks * 4
        self.fours = self.numDecks * 4
        self.threes = self.numDecks * 4
        self.twos = self.numDecks * 4

        self.cards = []
        for i in range (self.numDecks):
            for suit in ["Hearts", "Spades", "Clubs", "Diamonds"]:
                for val in range (1,14):
                    self.cards.append(Card(val,suit))
        self.shuffle()

    def __init__(self):
        self.numDecks = 1
        self.setup()

    def pull_card(self):
        card = self.cards.pop(0)
        
        pullcard_val = card.getVal()

        #probably a more elegant way of doing this
        if pullcard_val == 1:
            self.aces -= 1
        elif pullcard_val == 2:
            self.twos -= 1
        elif pullcard_val == 3:
            self.threes -= 1
        elif pullcard_val == 4:
            self.fours -= 1
        elif pullcard_val == 5:
            self.fives -= 1
        elif pullcard_val == 6:
            self.sixes -= 1
        elif pullcard_val == 7:
            self.sevens -= 1
        elif pullcard_val == 8:
            self.eights -= 1
        elif pullcard_val == 9:
            self.nines -= 1
        elif pullcard_val == 10:
            self.tens -= 1

        return card

    def print(self):
        for card in self.cards:
            print(card.abrev_str())

    def get_csv(self):
        return [self.aces, self.tens, self.nines, self.eights, self.sevens, self.sixes, self.fives, self.fours, self.threes, self.twos]