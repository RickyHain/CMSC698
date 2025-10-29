from ..Card import Card
from ..Deck import Deck
from ..Hand import Hand
from ..Players.CardCounter import CardCounter

import csv

class DataTracker(object):
    player_hand = Hand()
    dealer_hand = Hand()
    deck: Deck
    headers = ["Move", "Player", "Dealer", "Ace", "10", "9", "8", "7", "6", "5", "4", "3", "2", "Count active", "Cards in Deck", "Bet", "can_split", "has_ace", "cards_in_hands", "profit"]
    # headers = ["Move", "Player", "Dealer", "can_split", "has_ace"]
    bet_headers = ["Bet", "Count", "True Count", "Ace", "10", "9", "8", "7", "6", "5", "4", "3", "2" "Cards in Deck"]
    csv = []
    betting = []

    def __init__(self, p, dh, d):
        self.deck = d
        self.player:CardCounter = p
        self.dealer_hand = dh
        self.csv = [self.headers]
        self.betting = [self.bet_headers]

    def expand_csv_list(self,choice):
        hand = self.player.get_hand()
        line = [choice, hand.get_hand_val(), self.dealer_hand.get_hand_val()] + self.deck.get_csv() + [self.deck.get_true_count(), self.deck.get_deck_size(), hand.get_bet(), hand.can_split(), hand.has_ace(), hand.length(), self.player.get_proft()]
        # line = [choice, hand.get_hand_val(), self.dealer_hand.get_hand_val(), hand.can_split(), hand.has_ace()]
        self.csv.append(line)

    def update_csv_file(self):
        with open('output.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.csv)

    def update_betting_csv(self):
        with open('betting.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.betting)

    def expand_betting_csv(self):
        line = [self.player.get_hand().get_bet()] + [self.deck.get_true_count()] + self.deck.get_csv() + [self.deck.get_deck_size()]
        self.betting.append(line)
