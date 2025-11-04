import random
from .Card import Card


class Deck(object):
    numDecks = 1
    cards: list[Card] = []
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

    def manual_check(self):
        two = 0
        three = 0
        four = 0
        five = 0
        six = 0
        seven = 0
        eight = 0
        nine = 0
        ten = 0
        acee = 0

        for card in self.cards:
            if card.getVal() == 1:
                acee += 1
            elif card.getVal() ==2:
                two += 1
            elif card.getVal() == 3:
                three+= 1
            elif card.getVal() == 4:
                four+= 1
            elif card.getVal() == 5:
                five+= 1
            elif card.getVal() == 6:
                six+= 1
            elif card.getVal() == 7:
                seven+= 1
            elif card.getVal() == 8:
                eight+= 1
            elif card.getVal() == 9:
                nine+= 1
            elif card.getVal() == 10:
                ten+= 1

        print(f"2s: {two}, {self.twos}")
        print(f"3s: {three}, {self.threes}")
        print(f"4s: {four}, {self.fours}")
        print(f"5s: {five}, {self.fives}")
        print(f"6s: {six}, {self.sixes}")
        print(f"7s: {seven}, {self.sevens}")
        print(f"8s: {eight}, {self.eights}")
        print(f"9s: {nine}, {self.nines}")
        print(f"10s: {ten}, {self.tens}")
        print(f"As: {acee}, {self.aces}")


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

    def get_index(self, i:int):
        card: Card = self.cards[i]
        return card

    def get_true_count(self):

        return int(self.count/(float(len(self.cards)/52)))
    
    # def get_count(self):
    #     return self.count
    
    def get_count(self):
        deck = self
        return ((120-(deck.twos+deck.threes+deck.fours+deck.fives+deck.sixes))-(120-(deck.tens+deck.aces)))/(float(len(self.cards)/52))

    def print(self):
        for card in self.cards:
            print(card.abrev_str())

    def get_csv(self):
        return [self.aces, self.tens, self.nines, self.eights, self.sevens, self.sixes, self.fives, self.fours, self.threes, self.twos]
    
    def print_deck(self):
        for card in self.cards:
            print(str(card) + ", ")