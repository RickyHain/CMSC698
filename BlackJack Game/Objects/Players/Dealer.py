from Objects.Hand import Hand
from Objects.Card import Card
from Objects.Deck import Deck

class Dealer(object):
    def __init__(self, deck:Deck):
        self.hand: Hand = Hand()
        self.hide_card: Card = None
        self.deck:Deck = deck
        self.test_hand: Hand = Hand()
            
    def evaluate(self):
        # print(f"HIDE CARD: {str(self.hide_card)}")
        self.hand.append(self.hide_card)
            
        while(self.hand.get_hand_val()<17):
            self.hand.append(self.deck.pull_card())

    def look_forward(self, index):
        test_hand = Hand()
        for card in self.test_hand.get_cards():
            test_hand.append(card)

        i:int = index

        while(test_hand.get_hand_val()<17):
            try:
                test_hand.append(self.deck.get_index(i))
            except:
                break
            i += 1

        return test_hand.get_hand_val()
    
    def draw_card(self, card:Card):
        if self.hide_card is None:
            self.hide_card = card
        else:
            self.hand.append(card)

    def set_test_hand(self, hand:Hand):
        self.test_hand = hand

    def reset(self):
        self.hide_card: Card = None
        self.hand.reset()

    def get_hand(self):
        return self.hand
    
    def get_hand_val(self):
        return self.hand.get_hand_val()
    
    def get_full_hand_val(self):
        t: Hand = Hand()
        for card in self.hand.get_cards():
            t.append(card)

        t.append(self.hide_card)

        return t.get_hand_val()