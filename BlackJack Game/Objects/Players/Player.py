from Objects.Hand import Hand
from Objects.Card import Card


class Player(object):
    def __init__(self, max_bet, min_bet):
        self.hand_index = 0
        self.total_hands = 0
        self.hands: list[Hand] = []
        self.max_bet = max_bet
        self.min_bet = min_bet
        self.profit:int = 0

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
        current_hand = self.hands[self.hand_index]

        if current_hand.length() == 1:
            return "C"

        if current_hand.can_split():                                            #Player has all 4 options (2 cards of same value)
            move = input("(H)it, (S)tand, or (D)ouble or (Sp)lit: ").upper()
            if(move == "H" or move == "S" or move=="D" or move == "SP"):
                return move
        elif current_hand.length() == 2:                                        #Player has 3 options (2 cards of different value)
            move = input("(H)it, (S)tand, or (D)ouble: ").upper()
            if(move == "H" or move == "S" or move=="D"):
                return move
        else:                                                                   #Player has 2 options (more than 2 cards)
            move = input("(H)it, (S)tand: ").upper()
            if(move == "H" or move == "S"):
                return move

        return self.hit_stand()
    
    def place_bet(self):
        try:
            bet = int(input("Place bet (int): "))

            if (bet<self.min_bet):
                bet = self.min_bet
            if (bet>self.max_bet):
                bet = self.max_bet

            self.hands.append(Hand(bet))
            self.total_hands +=1
        except:
            self.place_bet()

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




    