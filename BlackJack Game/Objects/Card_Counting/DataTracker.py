from ..Card import Card
from ..Deck import Deck
from ..Hand import Hand
import csv

class DataTracker(object):
    player_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()
    headers = ["Hit?", "Player", "Dealer", "Ace", "10", "9", "8", "7", "6", "5", "4", "3", "2", "Top"]
    csv = []

    def __init__(self, ph, dh, d):
        self.deck = d
        self.player_hand = ph
        self.dealer_hand = dh
        self.csv = [self.headers]

    def expand_csv_list(self):
        line = return_play_details(self.player_hand, self.dealer_hand,self.deck)
        self.csv.append(line)

    def update_csv_file(self):
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.csv)

def return_play_details(player_hand, dealer_hand, deck):
    top_card_val = deck.get_top_card().getVal()
    hit_bool = False 
    if (top_card_val+player_hand.get_hand_val() <= 21): #don't hit unless the next card keeps hand under 21 (not considering ace value neccesarily)
        hit_bool = True
    return [hit_bool, player_hand.get_hand_val(), dealer_hand.get_hand_val()] + deck.get_csv() + [top_card_val]
          #[Hit? (T/F), player_hand_value, dealer_hand_value, Aces left, 10/J/Q/K's left, 9s left , ..., 2s left]