from .Deck import Deck
from .Card import Card
from .Hand import Hand
from .Players.Dealer import Dealer
from .Players.Player import Player
from .Players.BasicStrategy import BasicStrategy
from .Players.TestPlayer import TestPlayer
from .Players.CardCounter import CardCounter
from .Players.Cheater import Cheater
from .Players.SupervisedAI import SupervisedAI

from .Card_Counting.DataTracker import DataTracker

import os

class Game():
    #Intitalizing variables depending on specificaation in "black_jack.py"
    def __init__(self,player_type = "p", number_decks = 6, max_bet = 500, min_bet = 10):
        #Specifications for gameplay
        self.num_decks: int = number_decks
        self.deck: Deck = Deck(number_decks)
        self.deck.print_deck()

        #Dealer Specifications
        self.dealer:Dealer = Dealer(self.deck)
        self.dealer_hand: Hand = self.dealer.get_hand()
        self.dealer_wins: int = 0

        #Player Specifications
        self.player: Player = Player(max_bet, min_bet)
        if player_type == "bs":
            self.player: BasicStrategy = BasicStrategy(max_bet, min_bet, self.dealer_hand)
        elif player_type == "cc":
            self.player: CardCounter = CardCounter(max_bet, min_bet, self.dealer_hand, self.deck)
        elif player_type == "ch":
            self.player: Cheater = Cheater(max_bet, min_bet, self.dealer, self.deck)
        elif player_type == "ai":
            self.player: SupervisedAI = SupervisedAI(max_bet, min_bet, self.dealer_hand, self.deck)
        self.player_hand: Hand = Hand()
        self.player_wins: int = 0
            
        self.dt = DataTracker(self.player,self.dealer_hand,self.deck)

    def start_game(self):
        self.player.place_bet()
        self.dt.expand_betting_csv()
        self.player_hand = self.player.get_hand()

        self.player_hand.append(self.deck.pull_card())
        self.dealer.draw_card(self.deck.pull_card())
        # self.dealer_hand.append(self.deck.pull_card())
        self.player_hand.append(self.deck.pull_card())
        self.dealer.draw_card(self.deck.pull_card())

        if self.player.all_done(): #in case of blackjack
            self.dealer.evaluate()
        else:
            self.hit_loop()

    def hit_loop(self):
        self.player_hand = self.player.get_hand()
        # self.print_console(type=0)

        choice = self.player.hit_stand()
        if choice != "C":
            self.dt.expand_csv_list(choice)

        if choice == "H":
            self.player_hand.hit(self.deck.pull_card())
        elif choice == "S":
            self.player_hand.stand()
        elif choice == "D":
            self.player_hand.double(self.deck.pull_card())
        elif choice == "SP":
            self.player.split()
        elif choice == "C":
            self.player_hand.append(self.deck.pull_card())

        if self.player.all_done():
            self.dealer.evaluate()
            # self.end_game()
        else:
            try:
                self.hit_loop()
            except KeyboardInterrupt:
                print(f"Has Ace: {self.player_hand.has_ace()}     Can Split: {self.player_hand.can_split()}")

    def dealer_evaluate(self):
        d_val = self.dealer_hand.get_hand_val()

        while(d_val<17):
            self.dealer_hand.append(self.deck.pull_card())
            d_val = self.dealer_hand.get_hand_val()


    def end_game(self):
        d_val = self.dealer_hand.get_hand_val()
        p_val = self.player.get_hand().get_hand_val()

        if(p_val>21):                           #player bust
            self.dealer_wins+=1
            self.print_console(type=1)
        elif(d_val>21):                         #dealer bust
            self.player_wins+=1
            self.print_console(type=2)
        elif(p_val>d_val):                      #player higher
            self.dealer_wins+=1
            self.print_console(type=3)
        elif(d_val>p_val):                      #dealer higher
            self.player_wins+=1
            self.print_console(type=4)
        elif(d_val==p_val):                     #draw
            self.print_console(type=5)
        
    def reset_game(self):
        self.player.reset(self.dealer_hand) #player.reset also adds and subtracts hand bets for the player
        self.dealer.reset()
        self.start_game()

    def reset_player(self):
        self.player.reset_profit()

    def print_console(self, type):
        os.system("cls")
        print(f"Hand Bet: {str(self.player_hand.get_bet())}  Total Profit: {str(self.player.get_proft())}   Count: {round(self.deck.get_true_count(),3)}")
        if (type == 0): #hit_loop
            print(f"Dealer - {self.dealer_hand.get_hand_val_print()}\n{self.dealer_hand}\nYou - {self.player_hand.get_hand_val_print()} \n{self.player_hand}")
        elif(type==1): #Dealer Win (player bust)
            print(f"Dealer WINS!\nDealer - {self.dealer_hand.get_hand_val()}\n{self.dealer_hand}\nYou - {self.player_hand.get_hand_val()} BUST\n{self.player_hand}")
        elif(type==2): #Player win (dealer bust)
            print(f"You WIN!\nDealer - {self.dealer_hand.get_hand_val()} BUST\n{self.dealer_hand}\nYou - {self.player_hand.get_hand_val()} \n{self.player_hand}")
        elif(type==3): #Player Win (higher)
            print(f"You WIN!\nDealer - {self.dealer_hand.get_hand_val()}\n{self.dealer_hand}\nYou - {self.player_hand.get_hand_val()} \n{self.player_hand}")
        elif(type==4): #Dealer Win (higher)
            print(f"Dealer WINS!\nDealer - {self.dealer_hand.get_hand_val()} \n{self.dealer_hand}\nYou - {self.player_hand.get_hand_val()} \n{self.player_hand}")
        elif(type==5): #Draw
            print(f"DRAW\nDealer - {self.dealer_hand.get_hand_val()}\n{self.dealer_hand}\nYou - {self.player_hand.get_hand_val()} \n{self.player_hand}")

    def update_csv(self):
        self.dt.update_csv_file()
        self.dt.update_betting_csv()
        # self.player.update_csv_file()

    def count_debug(self):
        self.deck.manual_check()
