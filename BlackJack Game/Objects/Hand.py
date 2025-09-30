from .Card import Card

class Hand():
    hand_value = 0

    def get_hand_val(self):
        return self.hand_value

    def __init__(self):
        value = 0
        self._data = []

    def append(self, card):
        self._data.append(card)
        self.evaluate(card)

    def evaluate(self, card):
        self.hand_value += card.getVal()

    def reset(self):
        self.__init__

    def __str__(self):
        return_str = "| "
        for card in self._data:
            return_str += (card.abrev_str() + " | ")

        return return_str