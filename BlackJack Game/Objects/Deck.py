import random
from .Card import Card


class Deck(object):
    numDecks = 1
    cards = []
    count = 0
    

    def shuffle(self):
        random.shuffle(self.cards)

    def setNumDecks(self,n):
        self.numDecks = n
        self.setup()

    def get_deck_size(self):
        return len(self.cards)

    def setup(self):
        self.count = 0
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
                    self.cards.append(Card((val),suit))
        self.shuffle()

    def __init__(self, n):
        self.numDecks = n
        self.setNumDecks(n)
        self.setup()

    def pull_card(self):
        card: Card
        if(len(self.cards) >= 104 and self.numDecks >= 4): #If there are more than 2 decks left keep drawing
            card = self.cards.pop(0)
        else: #If there's less, we reshuffle at total numDecks and draw the top card 
            self.setup()
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

        if pullcard_val in [10,1]:
            self.count -= 1
        elif pullcard_val in [2,3,4,5,6]:
            self.count +=1

        return card

    def get_top_card(self):
        return self.cards[0]

    def get_true_count(self):
        return -round(float(self.count/(float(len(self.cards)/52))),3)
    
    def get_count(self):
        return self.count
    
    def get_count_calc(self):
        deck = self
        return ((deck.twos+deck.threes+deck.fours+deck.fives+deck.sixes)-(deck.tens+deck.aces))/(float(len(self.cards)/52))

    def print(self):
        for card in self.cards:
            print(card.abrev_str())

    def get_csv(self):
        return [self.aces, self.tens, self.nines, self.eights, self.sevens, self.sixes, self.fives, self.fours, self.threes, self.twos]