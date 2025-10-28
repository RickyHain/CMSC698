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

        self.split_table: list[list[str]]
        self.soft_table: list[list[str]] 
        self.hard_table: list[list[str]] 
        self.split_table, self.soft_table, self.hard_table = setup_tables()

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
        d_index = self.dealer_hand.get_hand_val() - 2 #dealer idex 0 is at value of 2
        bet_table: list[list[str]]
        p_index:int
        test:str

        #Statement to make make sure that we're not betting on hands less than 2 cards
        if current_hand.length() == 1:
            return "C"                                          #C means new card

        if current_hand.can_split():
            bet_table = self.split_table
            p_index = int((current_hand.get_hand_val()/2) - 2)      #hand total is 2*pair and index 0 starts at a pair of 2's 
        elif current_hand.is_soft():
            bet_table = self.soft_table
            p_index = current_hand.get_hand_val()-13            #index 0 starts at value of 13 (AA/12 covered by split table)
        else:
            bet_table = self.hard_table
            p_index = current_hand.get_hand_val()-5             #index 0 starts at value of 5

        play:str = bet_table[p_index][d_index]

        if play == "D" and current_hand.length()!=2:
            play = "H"

        if play == "DS":
            if current_hand.length() == 2:
                play = "D"
            else:
                play = "S"

        return play

    
    def place_bet(self):
        true_count = self.deck.get_true_count()
        TC_max = 5.0
        k = (self.max_bet-self.min_bet)/(TC_max-1)

        if true_count <= 1:
            bet = self.min_bet
        else:
            bet = self.min_bet + (true_count-1) * k
            bet = min(bet, self.max_bet)
        bet = round(bet / 5) * 5

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

    def reset_profit(self):
        self.profit = 0

    def get_hand(self):
        return self.hands[self.hand_index]


def setup_tables():
    split = [
            # 2    3    4    5    6    7    8    9   10    A
            ["H" ,"H" ,"SP","SP","SP","SP","H" ,"H" ,"H" ,"H" ], #2's
            ["H" ,"H" ,"SP","SP","SP","SP","H" ,"H" ,"H" ,"H" ], #3's
            ["H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ], #4's
            ["D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"H" ,"H" ], #5's
            ["H" ,"SP","SP","SP","SP","H" ,"H" ,"H" ,"H" ,"H" ], #6's
            ["SP","SP","SP","SP","SP","SP","H" ,"H" ,"H" ,"H" ], #7's
            ["SP","SP","SP","SP","SP","SP","SP","SP","SP","SP"], #8's
            ["SP","SP","SP","SP","SP","S" ,"SP","SP","S" ,"S" ], #9's
            ["S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ], #10's
            ["SP","SP","SP","SP","SP","SP","SP","SP","SP","SP"]  #Aces
        ]

    soft = [
            # 2    3    4    5    6    7    8    9   10    A
            ["H" ,"H" ,"H" ,"D" ,"D" ,"H" ,"H" ,"H" ,"H" ,"H"], #13
            ["H" ,"H" ,"H" ,"D" ,"D" ,"H" ,"H" ,"H" ,"H" ,"H"], #14
            ["H" ,"H" ,"D" ,"D" ,"D" ,"H" ,"H" ,"H" ,"H" ,"H"], #15
            ["H" ,"H" ,"D" ,"D" ,"D" ,"H" ,"H" ,"H" ,"H" ,"H"], #16
            ["H" ,"D" ,"D" ,"D" ,"D" ,"H" ,"H" ,"H" ,"H" ,"H"], #17
            ["H" ,"DS","DS","DS","DS","H" ,"H" ,"H" ,"H" ,"H"], #18
            ["H" ,"D" ,"D" ,"D" ,"D" ,"H" ,"H" ,"H" ,"H" ,"H"], #19
            ["D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"H" ,"H"]  #20
        ]
    
    hard = [
            # 2    3    4    5    6    7    8    9   10    A
            ["H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H"], #5
            ["H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H"], #6
            ["H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H"], #7
            ["H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H" ,"H"], #8
            ["H" ,"D" ,"D" ,"D" ,"D" ,"H" ,"H" ,"H" ,"H" ,"H"], #9
            ["D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"H" ,"H"], #10
            ["D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D" ,"D"], #11
            ["H" ,"H" ,"S" ,"S" ,"S" ,"H" ,"H" ,"H" ,"H" ,"H"], #12
            ["S" ,"S" ,"S" ,"S" ,"S" ,"H" ,"H" ,"H" ,"H" ,"H"], #13
            ["S" ,"S" ,"S" ,"S" ,"S" ,"H" ,"H" ,"H" ,"H" ,"H"], #14
            ["S" ,"S" ,"S" ,"S" ,"S" ,"H" ,"H" ,"H" ,"H" ,"H"], #15
            ["S" ,"S" ,"S" ,"S" ,"S" ,"H" ,"H" ,"H" ,"H" ,"H"], #16
            ["S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S"], #17
            ["S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S"], #18
            ["S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S"], #19
            ["S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S" ,"S"]  #20
        ]
    
    return split,soft,hard

