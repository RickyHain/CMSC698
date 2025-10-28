from .Card import Card

class Hand():
    bet_value:int = 0
    hand_value = 0
    ace_hand_value = 10
    black_jack: bool = False
    split: bool = False
    ace: bool = False
    done: bool = False

    #Initializing variables of a new hand
    def __init__(self, bet=0):
        self.bet_value:int = bet
        self.hand_value = 0
        self.ace_hand_value = 10
        self.black_jack = False
        self.split = False
        self.ace = False
        self.done = False
        self._data: list[Card] = []

    def get_bet(self):
        return self.bet_value

    #Will return the highest value of the hand that is under 21 (depending on if there's an ace or not)
    def get_hand_val(self): 
        if (self.ace):
            if (self.ace_hand_value<=21):
                return self.ace_hand_value
        return self.hand_value

    #Will return the value as a string to print
    #If theres an ace you'll get a (X or X+10) assuming the higher is under 21
    def get_hand_val_print(self):
        if (self.ace):
            if (self.ace_hand_value<21):
                return f"{self.hand_value} or {self.ace_hand_value}"
            if(self.ace_hand_value==21):
                return f"{self.ace_hand_value}"
        return f"{self.hand_value}"
    
    #Logic statements for having an ace or being able to split
    def is_soft(self):
        return self.ace_hand_value<=21 and self.ace

    def has_ace(self):
        return self.ace
    
    def can_split(self):
        return self.split
    
    def hand_over(self):
        return self.done
    
    def is_black_jack(self):
        return self.black_jack

    #Append adds new cards to the hand
    def append(self, card):
        if(card.getVal() == 1):
            self.ace = True

        if(len(self._data)!=2):
            self.split = False

        self._data.append(card)
        self.evaluate(card)

    #updates the values of the hand
    def evaluate(self, card):
        self.hand_value += card.getVal()
        self.ace_hand_value += card.getVal()

        # print(f" self.gethandvalue(): {self.get_hand_val()}")
        if(len(self._data)==2):
            if (self.hand_value == 21):
                self.done = True
                self.bet_value *= 1.5
            
            if (self._data[0].getVal() == self._data[1].getVal()):
                self.split = True
                

        if(self.get_hand_val() >= 21):                                  #Can't hit anymore once you're at or above 21
            self.done = True

    def reset(self):
        self.__init__()

    #PLAYER CHOICES \/
    def hit(self, card):
        self.append(card)

    def stand(self):
        self.done = True

    def double(self, card):
        self.append(card)
        self.bet_value *= 2
        self.done = True

    def split_hand(self):
        self.hand_value-=self._data[-1].getVal()
        self.ace_hand_value-=self._data[-1].getVal()
        self.split = False
        return self._data.pop()
    #PLAYER CHOICES /\

    def length(self):
        return len(self._data)

    #adds print() functionality
    def __str__(self):
        return_str = "| "
        for card in self._data:
            return_str += (card.abrev_str() + " | ") #card values will be abreviated and speparated by |'s

        return return_str