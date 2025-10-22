from ..Hand import Hand
import numpy as np

class AveragePlayer(object):
    #The avaerage player will be represented by "basic strategy" which is the mathematically best way to play (Without card counting)

    def __init__(self, p_hand, d_hand):
        self.player_hand = p_hand
        self.dealer_hand = d_hand

    def place_bet(self):
        mu = 0.0
        sigma = 0.7
        min_bet = 10
        max_bet = 500

        bet = np.random.lognormal(mu, sigma)
        bet = (bet / 3) * (max_bet - min_bet) + min_bet  # scale/shift
        bet = round(bet / 5) * 5

        return bet

    def hit_stand(self):
        #True = Hit      False = Stand
        p_score = self.player_hand.get_hand_val()
        d_score = self.dealer_hand.get_hand_val()

        #Logic is based off of the basic strategy table
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
            