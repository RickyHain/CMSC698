from .Deck import Deck
from .Card import Card
from .Hand import Hand

class Game():
    num_players = int #maybe do later
    num_decks = int
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()

    def __init__(self,number_players = 1, number_decks = 2):
        self.num_players = number_players
        self.num_decks = number_decks
        self.deck.setNumDecks(number_decks)
        self.start_game()

    def start_game(self):
        self.player_hand.append(self.deck.pull_card())
        self.dealer_hand.append(self.deck.pull_card())
        self.player_hand.append(self.deck.pull_card())
        self.print_console()
        self.game_loop()

    def game_loop(self):
        hit = hit_stand()
        if hit:
            print('you hit')


    def print_console(self):
        print(f"Dealer - {self.dealer_hand.get_hand_val()}\n{self.dealer_hand}\nYou - {self.player_hand.get_hand_val()} \n{self.player_hand}")

def hit_stand():
    move = input("(H)it or (S)tand: ").upper()
    if(move == "H" or move == "S"):
        if (move == "H"):
            return True
        else:
            return False
    else:
        hit_stand()
