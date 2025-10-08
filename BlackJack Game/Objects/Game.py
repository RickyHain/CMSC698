from .Deck import Deck
from .Card import Card
from .Hand import Hand
from .Card_Counting.DataTracker import DataTracker
import os

class Game():
    num_players = int #maybe do later
    num_decks = int
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    player_wins = 0
    dealer_wins = 0

    def __init__(self,number_players = 1, number_decks = 2):
        self.dt = DataTracker(self.player_hand,self.dealer_hand,self.deck)
        self.num_players = number_players
        self.num_decks = number_decks
        self.deck.setNumDecks(number_decks)
        self.start_game()

    # Getters
    def get_deck(self):
        return self.deck

    def get_player_hand(self):
        return self.player_hand

    def get_dealer_hand(self):
        return self.dealer_hand
    # Getters


    def start_game(self):
        self.player_hand.append(self.deck.pull_card())
        self.dealer_hand.append(self.deck.pull_card())
        self.player_hand.append(self.deck.pull_card())
        self.player_evaluate()

    def game_loop(self):
        self.dt.expand_csv_list()
        self.print_console(type=0)
        hit = hit_stand(self.deck,self.dt)
        if hit:
            print('you hit')
            self.player_hand.append(self.deck.pull_card())
            self.player_evaluate()
        else:
            print('you stood')
            self.dealer_evaluate()

    def player_evaluate(self):
        p_val = self.player_hand.get_hand_val()

        if(p_val<21):
            #print('less')
            self.game_loop()
        elif(p_val==21):
            #print('equal')
            self.dealer_evaluate()
        else:
            #print('more')
            self.end_game()

    def dealer_evaluate(self):
        d_val = self.dealer_hand.get_hand_val()

        while(d_val<17):
            self.dealer_hand.append(self.deck.pull_card())
            d_val = self.dealer_hand.get_hand_val()

        self.end_game()

    def end_game(self):
        d_val = self.dealer_hand.get_hand_val()
        p_val = self.player_hand.get_hand_val()

        if(p_val>21): #player bust
            self.dealer_wins+=1
            self.print_console(type=1)
        elif(d_val>21): #dealer bust
            self.player_wins+=1
            self.print_console(type=2)
        elif(p_val>d_val): #player higher
            self.dealer_wins+=1
            self.print_console(type=3)
        elif(d_val>p_val): #dealer higher
            self.player_wins+=1
            self.print_console(type=4)
        elif(d_val==p_val): #draw
            self.print_console(type=5)
        self.reset_game()
        
    def reset_game(self):
        play_again()
        self.player_hand.reset()
        self.dealer_hand.reset()
        self.start_game()

    def print_console(self, type):
        os.system("cls")
        if (type == 0): #Game_loop
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


   
def hit_stand(deck,data_tracker):
    move = input("(H)it or (S)tand: ").upper()
    if(move == "P"):
        print(deck.get_csv())

    if(move == "U"):
        data_tracker.update_csv_file()

    if(move == "H" or move == "S"):
        if (move == "H"):
            return True
        else:
            return False
    else:
        return hit_stand(deck,data_tracker)

def play_again():
    play_again = input("Enter to play again").upper()
