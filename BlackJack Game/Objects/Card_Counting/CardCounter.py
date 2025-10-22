"""
The card counter plays basic strategy while simulataniously keeping track of the number of high value cards relative
to the total cards left in the deck. At the right moment, they will hit regardless of what basic strategy suggests

The card counter adjust their betting based on the running count.

This Player object reflects how a human would card count in real time
"""
from ..Hand import Hand
from ..Card import Card
from ..Deck import Deck

import numpy as np

class CardCounter(object):
    def __init__(self, p_hand, d_hand):
        self.player_hand = p_hand
        self.dealer_hand = d_hand
        self.running_count = 0
        self.decks

    def hit_stand(self):
        #True = Hit      False = Stand
        p_score = self.player_hand.get_hand_val()
        d_score = self.dealer_hand.get_hand_val()

        if (self.player_hand.has_ace() == False): #If player has no Ace
            if (p_score <= 11):
                return True
            elif (p_score == 12):
                if (d_score <= 3 or d_score >=7):
                    return True
                else:
                    return False
            elif (p_score <= 16):
                if (d_score<=6):
                    return False
                else:
                    return True
            if (p_score >= 17):
                return True
        else:                                               #If player has an ace
            if (p_score<=16):
                return True
            elif (p_score == 17):
                if (d_score <= 8):
                    return False
                else:
                    return True
            else:
                return False
            
    def bet(self):
        #For betting, I'm assuming the average player bets near the minimum and have a normal distribution to get so varying results
        pass