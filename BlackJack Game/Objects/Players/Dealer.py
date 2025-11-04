from Objects.Hand import Hand
from Objects.Card import Card
from Objects.Deck import Deck

class Dealer(object):
    def __init__(self, deck:Deck):
        self.hand: Hand = Hand()
        self.hide_card: Card = None
        self.deck:Deck = deck
            
    def evaluate(self):
        # print(f"HIDE CARD: {str(self.hide_card)}")
        self.hand.append(self.hide_card)
            
        while(self.hand.get_hand_val()<17):
            self.hand.append(self.deck.pull_card())

    def look_forward(self, index):
        test_hand: Hand = Hand()
        hand_cards = self.hand.get_cards()

        for card in hand_cards:
            test_hand.append(card)

        test_hand.append(self.hide_card)

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

    def reset(self):
        self.hide_card: Card = None
        self.hand.reset()

    def get_hand(self):
        return self.hand
    
    def get_hand_val(self):
        return self.hand.get_hand_val()