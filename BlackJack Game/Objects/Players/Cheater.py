from Objects.Hand import Hand
from Objects.Card import Card
from Objects.Deck import Deck
from ..Players.Dealer import Dealer
import numpy as np


class Cheater(object):
    def __init__(self, max_bet: int, min_bet: int,dealer:Dealer, deck:Deck):
        self.hand_index = 0
        self.total_hands = 0
        self.hands: list[Hand] = []
        self.max_bet = max_bet
        self.min_bet = min_bet
        self.moves = []
        self.bet = 0
        self.profit:int = 0
        self.dealer: Dealer = dealer
        self.deck: Deck = deck

    def get_proft(self):
        return self.profit
    
    def all_done(self):
        current_hand:Hand = self.hands[self.hand_index]
        if (current_hand.hand_over()):                          #If our current can no longer be played on (stood, bust, doubled down)
            if (len(self.hands) == self.hand_index+1):          #Check that we don't have any more hands from a split
                return True
            else:
                self.hand_index +=1                             #If we do, we update our index and return False
                return False
                  
        return False
            

    def hit_stand(self):
        current_hand:Hand = self.hands[self.hand_index]
        #Statement to make make sure that we're not betting on hands less than 2 cards
        if current_hand.length() == 1:
            return "C"                                          #C means new card

        return self.moves.pop(0)
    
    def place_bet(self):
        self.look_forward()

        self.hands.append(Hand(self.bet))
        self.total_hands +=1

    #!!!!Current issue is that we don't create hands until betting, but we want to look forward before betting!!!!
    def look_forward(self):
        moves: list[str] = []
        i: int = 0
        test_hand: Hand = Hand()
        hand_cards = self.get_hand().get_cards()

        for card in hand_cards:
            test_hand.append(card)

        test_hand.append(self.hide_card)

        while True:
            #what happens if we stand
            dealer_value = self.dealer.look_forward()
            if (test_hand.get_hand_val() <=21 and (dealer_value > 21 or (dealer_value < test_hand.get_hand_val()))):
                self.bet = self.max_bet
                moves.append("S")
                break


            #what happens if we hit
            test_hand.append(self.deck.get_index(i))
            if (test_hand.get_hand_val() <= 21):
                moves.append("H")
            else:
                moves.append("S")
                self.bet = self.min_bet
                break

        if moves == ["H","S"]:
            moves = ["D"]

        self.moves = moves

    def reset_profit(self):
        self.profit = 0

    def get_hand(self):
        return self.hands[self.hand_index]