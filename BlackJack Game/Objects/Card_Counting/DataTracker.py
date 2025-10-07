from ..Card import Card
from ..Deck import Deck
from ..Game import Game
from ..Hand import Hand
import csv

class DataTracker(object):
    game = Game()
    player_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()

    def __init__(self,g):
        self.game = g
        self.deck = g.get_deck()
        self.player_hand = g.get_player_hand()
        self.dealer_hand = g.get_dealer_hand()

    headers = ["Hit?", "Dealer", "Player", "Ace", "10", "9", "8", "7", "6", "5", "4", "3", "2"]

    def return_csv(self):
        top_card_val = self.deck[0].getVal
        hit_bool = False 
        if (top_card_val+self.player_hand.get_hand_val() <= 21): #don't hit unless the next card keeps hand under 21
            hit_bool = True
        return [hit_bool, self.player_hand.get_hand_val(), self.dealer_hand.get_hand_val()] + self.deck.get_csv()
               #[Hit? (T/F), player_hand_value, dealer_hand_value, Aces left, 10/J/Q/K's left, 9s left , ..., 2s left]