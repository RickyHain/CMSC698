from Objects.Hand import Hand
from Objects.Card import Card
from Objects.Deck import Deck
from ..Players.Dealer import Dealer
import csv

class Cheater(object):
    def __init__(self, max_bet: int, min_bet: int,dealer:Dealer, deck:Deck):
        self.hand_index = 0
        self.total_hands = 0
        self.hands: list[Hand] = []
        self.test_hand: Hand = Hand()
        self.max_bet = max_bet
        self.min_bet = min_bet
        self.moves = []
        self.bet = 0
        self.profit:int = 0
        self.dealer: Dealer = dealer
        self.deck: Deck = deck


        self.headers = ["Move", "Player", "Dealer", "can_split", "has_ace", "c1","c2","c3","c4"]
        self.csv = []
        self.move_chains = []
        self.csv.append(self.headers)

    def get_profit(self):
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

        self.expand_csv_list(self.moves[0])
        return self.moves.pop(0)
    
    def place_bet(self):
        self.set_test_hands()
        self.look_forward()

        self.hands.append(Hand(self.bet))
        self.total_hands +=1

    #!!!!Current issue is that we don't create hands until betting, but we want to look forward before betting!!!!
    def look_forward(self):
        moves: list[str] = []
        i: int = 4
        test_hand = self.test_hand

        while True:
            #what happens if we stand
            dealer_value = self.dealer.look_forward(i)
            if (test_hand.get_hand_val() <=21 and (dealer_value > 21 or dealer_value < test_hand.get_hand_val())):
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
            i+=1

        if moves == ["H","S"] and self.bet == self.max_bet:
            moves = ["D"]

        self.moves = moves
        self.move_chains.append(moves.copy())

    def set_test_hands(self):
        test_dealer: Hand = Hand()
        self.test_hand = Hand()

        self.test_hand.append(self.deck.get_index(0))
        self.test_hand.append(self.deck.get_index(2))

        test_dealer.append(self.deck.get_index(1))
        test_dealer.append(self.deck.get_index(3))

        self.dealer.set_test_hand(test_dealer)

    def reset(self, dealer_hand:Hand):
        dealer_val = dealer_hand.get_hand_val()

        for hand in self.hands:
            player_val = hand.get_hand_val()

            if player_val > 21:
                self.expand_csv_list("L")
                self.profit -= hand.get_bet()
            elif dealer_val > 21:
                self.expand_csv_list("W")
                self.profit += hand.get_bet()
            else:
                if player_val > dealer_val:
                    self.expand_csv_list("W")
                    self.profit += hand.get_bet()
                elif player_val < dealer_val:
                    self.expand_csv_list("L")
                    self.profit -= hand.get_bet()
                else:
                    self.expand_csv_list("T")    

        self.hand_index = 0
        self.total_hands = 0
        self.hands: list[Hand] = []
        self.moves:str = []

    def reset_profit(self):
        self.profit = 0

    def get_hand(self):
        return self.hands[self.hand_index]
    

    def expand_csv_list(self,choice):
        hand = self.get_hand()
        line = [choice, hand.get_hand_val(), self.dealer.get_full_hand_val(), hand.can_split(), hand.has_ace(), self.deck.get_index(0).abrev_str(),self.deck.get_index(1).abrev_str(),self.deck.get_index(2).abrev_str(),self.deck.get_index(3).abrev_str()]
        self.csv.append(line)

    def update_csv_file(self):
        with open('cheater_out.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.csv)

        with open('move_chains.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.move_chains)