from Objects.Hand import Hand
from Objects.Card import Card
from Objects.Deck import Deck
import numpy as np


class CardCounter(object):
    def __init__(self, max_bet, min_bet,dealer_hand, deck):
        self.hand_index = 0
        self.total_hands = 0
        self.hands: list[Hand] = []
        self.max_bet = max_bet
        self.min_bet = min_bet
        self.profit:int = 0
        self.dealer_hand: Hand = dealer_hand
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
        #True = Hit      False = Stand
        current_hand:Hand = self.hands[self.hand_index]
        p_score = current_hand.get_hand_val()
        d_score = self.dealer_hand.get_hand_val()

        if current_hand.length() == 1:
            return "C"

        #THERE ARE ILLEGAL DOUBLES
        if current_hand.can_split():                    #Split Logic
            if p_score in [4, 6]:           #Pair 2s or 3s
                if d_score <=7:
                    return "SP"
                else:
                    return "H"
            elif p_score == 8:
                if d_score in [5,6]:
                    return "SP"
                else:
                    return "H"
            elif p_score == 10:
                if d_score <=9:
                    return "D"
                else:
                    return "H"
            elif p_score == 12 and not current_hand.has_ace():
                if d_score <=6:
                    return "SP"
                else:
                    return "H"
            elif p_score == 14:
                if d_score <=7:
                    return "SP"
                else:
                    return "H"
            elif p_score == 16:
                if d_score <=9:
                    return "SP"
                else:
                    return "H"
            elif p_score == 18:
                if d_score in [7,10,11]:
                    return "S"
                else:
                    return "SP"
            elif p_score == 20:
                return "S"
            elif p_score == 12 and not current_hand.has_ace():
                if d_score == 11:
                    return "SP"
                else:
                    return "H"
        if current_hand.has_ace() and current_hand.get_hand_val() > 12:                      #ACE & CARD Logic
            if p_score in [13, 14]:         #ACE, 2/3
                if d_score in [5,6]:
                    return "D"
                else:
                    return "H"
            if p_score in [15, 16]:         #ACE, 4/5
                if d_score in [4,5,6]:
                    return "D"
                else:
                    return "H"
            if p_score == 17:               #ACE, 6
                if d_score in [3,4,5,6]:
                    return "D"
                else:
                    return "H"
            if p_score == 18:               #ACE, 7
                if d_score <=6 and not d_score==1:
                    return "D"
                elif d_score in [1,7,8]:
                    return "S"
                else:
                    return "H"
            else:               #ACE, 8   |   ACE, 9   |   ACE, 10 == Blackjack | ACE, ACE is covered in split logic
                return "S"                 
        else:                                           #NO SPLIT and NO ACE
            if p_score <= 8:
                return "H"
            elif p_score == 9:
                if d_score in [3,4,5,6]:
                    return "D"
                else:
                    return "H"
            elif p_score  in [10,11]:
                if d_score <= 9:
                    return "D"
                else:
                    return "H"
            elif p_score == 12:
                if d_score in [4,5,6]:
                    return "S"
                else:
                    return "H"
            elif p_score in [13,14,15,16]:
                if d_score <= 6:
                    return "S"
                else:
                    return "H"
            else:
                return "S"
    
    def place_bet(self):
        true_count = self.deck.get_true_count()
        bet = self.min_bet

        if true_count > 1.0:
            bet = self.max_bet

        self.hands.append(Hand(bet))
        self.total_hands +=1

    def split(self):
        current_hand:Hand = self.hands[self.hand_index]
        
        split_card: Card = current_hand.split_hand()
        split_hand: Hand = Hand(current_hand.get_bet())               
        split_hand.append(split_card)
        self.hands.append(split_hand)


    def reset(self, dealer_hand:Hand):
        dealer_val = dealer_hand.get_hand_val()

        for hand in self.hands:
            player_val = hand.get_hand_val()

            if player_val > 21:
                self.profit -= hand.get_bet()
            elif dealer_val > 21:
                self.profit += hand.get_bet()
            else:
                if player_val > dealer_val:
                    self.profit += hand.get_bet()
                elif player_val < dealer_val:
                    self.profit -= hand.get_bet()

        self.hand_index = 0
        self.total_hands = 0
        self.hands: list[Hand] = []


    def get_hand(self):
        return self.hands[self.hand_index]




    