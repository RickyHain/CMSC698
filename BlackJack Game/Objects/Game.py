from .Deck import Deck
from .Card import Card
from .Hand import Hand
from .Players.Player import Player
from .Players.BasicStrategy import BasicStrategy
from .Players.TestPlayer import TestPlayer
from .Players.CardCounter import CardCounter

from .Card_Counting.DataTracker import DataTracker
from .Card_Counting.AveragePlayer import AveragePlayer
from .Card_Counting.Cheater import Cheater

import os

class Game():
    #Intitalizing variables depending on specificaation in "black_jack.py"
    def __init__(self,number_players = 1, number_decks = 6, max_bet = 500, min_bet = 10):
        #Used to generate csv data for each choice
        #our diffetent player objects
        # self.ch = Cheater(self.player_hand,self.dealer_hand,self.deck)
        # self.ap = AveragePlayer(self.player_hand, self.dealer_hand)
        self.dealer_hand: Hand = Hand()
        self.player_wins: int = 0
        self.dealer_wins: int = 0
        self.player_hand: Hand = Hand()

        #Specifications for gameplay
        self.num_players: int = number_players
        self.num_decks: int = number_decks
        self.deck: Deck = Deck(number_decks)

        self.player: CardCounter = CardCounter(max_bet, min_bet, self.dealer_hand, self.deck)
        # self.player: Player = Player(max_bet, min_bet)
        #self.player: BasicStrategy = BasicStrategy(max_bet, min_bet, self.dealer_hand)
        self.dt = DataTracker(self.player,self.dealer_hand,self.deck)

    def start_game(self):
        self.player.place_bet()
        self.dt.expand_betting_csv()
        self.player_hand = self.player.get_hand()

        self.player_hand.append(self.deck.pull_card())
        self.dealer_hand.append(self.deck.pull_card())
        self.player_hand.append(self.deck.pull_card())

        if self.player.all_done():
            self.dealer_evaluate()
        else:
            self.hit_loop()

    def hit_loop(self):
        self.player_hand = self.player.get_hand()
        self.print_console(type=0)

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
            self.dealer_evaluate()
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

        self.end_game()

    def end_game(self):
        d_val = self.dealer_hand.get_hand_val()
        p_val = self.player_hand.get_hand_val()

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
        self.player.reset(self.dealer_hand)
        self.dealer_hand.reset()
        self.start_game()
        

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
