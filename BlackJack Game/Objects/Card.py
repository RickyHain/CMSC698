class Card:
    def __init__(self, v, s):
        self.value = 0
        self.suit = ""
        self.setVal(v)
        self.setSuit(s)

    def setVal(self, v):
        self.value = v

    def setSuit(self, s):
        correct_suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
        if s in correct_suits:
            self.suit = s
        else:
            raise ValueError(f"Invalid suit: {s}")

    def getVal(self):
        if self.value > 10:
            return 10
        
        return self.value

    def getSuit(self):
        return self.suit

    def __str__(self):
        print_value = self.value
        if self.value > 10:
            if self.value == 11:
                print_value = "Jack"
            elif self.value == 12:
                print_value = "Queen"
            elif self.value == 13:
                print_value = "King"
            elif self.value == 14:
                print_value = "Ace"
        return f"{print_value} of {self.suit}"
    
    def abrev_str(self):
        print_value = self.value
        if self.value > 10:
            if self.value == 11:
                print_value = "J"
            elif self.value == 12:
                print_value = "Q"
            elif self.value == 13:
                print_value = "K"
            elif self.value == 14:
                print_value = "A"
        
        
        return f"{print_value}{self.suit[0]}"