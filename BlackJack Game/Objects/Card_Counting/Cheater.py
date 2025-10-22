#The Cheater knows the next card in the deck and will hit/stand accordingly
from ..Hand import Hand
from ..Card import Card
from ..Deck import Deck

class Cheater(object):
    #The avaerage player will be represented by "basic strategy" which is the mathematically best way to play (Without card counting)

    def __init__(self, p_hand, d_hand, deck):
        self.player_hand = p_hand
        self.dealer_hand = d_hand
        self.deck = deck

    def hit_stand(self):
        #True = Hit      False = Stand
        top_card_val = self.deck.get_top_card().getVal()
        p_score = self.player_hand.get_hand_val()
        hit_bool = False 
        if (top_card_val + p_score <= 21):
            hit_bool = True

        return hit_bool