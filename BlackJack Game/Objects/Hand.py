from .Card import Card

class Hand():
    hand_value = 0
    ace = False
    ace_hand_value = 10

    def get_hand_val(self):
        if (self.ace):
            if (self.ace_hand_value<=21):
                return self.ace_hand_value
        return self.hand_value

    def get_hand_val_print(self):
        if (self.ace):
            if (self.ace_hand_value<21):
                return f"{self.hand_value} or {self.ace_hand_value}"
            if(self.ace_hand_value==21):
                return f"{self.ace_hand_value}"
        return f"{self.hand_value}"

    def __init__(self):
        self.hand_value = 0
        self.ace_hand_value = 10
        self.ace = False
        self._data = []

    def append(self, card):
        if(card.getVal() == 1):
            self.ace = True
        self._data.append(card)
        self.evaluate(card)

    def evaluate(self, card):
        self.hand_value += card.getVal()
        self.ace_hand_value += card.getVal()

    def reset(self):
        self.__init__()

    def __str__(self):
        return_str = "| "
        for card in self._data:
            return_str += (card.abrev_str() + " | ")

        return return_str