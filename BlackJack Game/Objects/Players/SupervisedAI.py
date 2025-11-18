import torch
import torch.nn as nn
import torch.nn.functional as F
from Objects.Hand import Hand
from Objects.Deck import Deck

# -------------------------------
# Move model architecture (classification)
# -------------------------------
class CardCountingNet(nn.Module):
    def __init__(self, in_features=15, hidden1=128, hidden2=64, out_features=4):
        super().__init__()
        self.fc1 = nn.Linear(in_features, hidden1)
        self.bn1 = nn.BatchNorm1d(hidden1)
        self.fc2 = nn.Linear(hidden1, hidden2)
        self.bn2 = nn.BatchNorm1d(hidden2)
        self.dropout = nn.Dropout(0.3)
        self.fc3 = nn.Linear(hidden2, out_features)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        return self.fc3(x)

# -------------------------------
# Bet model architecture (regression)
# -------------------------------
class BettingNet(nn.Module):
    def __init__(self, in_features=10, hidden1=128, hidden2=64):
        super().__init__()
        self.fc1 = nn.Linear(in_features, hidden1)
        self.bn1 = nn.BatchNorm1d(hidden1)
        self.fc2 = nn.Linear(hidden1, hidden2)
        self.bn2 = nn.BatchNorm1d(hidden2)
        self.fc3 = nn.Linear(hidden2, 1)

    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = F.relu(self.bn2(self.fc2(x)))
        return self.fc3(x)

class SupervisedAI(object):
    def __init__(self, max_bet: int, min_bet: int, dealer_hand: Hand, deck: Deck):
        self.max_bet = max_bet
        self.min_bet = min_bet
        self.dealer_hand = dealer_hand
        self.deck = deck

        self.hands = []
        self.hand_index = 0
        self.total_hands = 0
        self.profit = 0


        # -------------------------------
        # Load Move Model
        # -------------------------------
        self.move_model = CardCountingNet()
        self.move_model.load_state_dict(torch.load("Models\move_model.pth", map_location="cpu"))
        self.move_model.eval()

        # -------------------------------
        # Load Bet Model
        # -------------------------------
        self.bet_model = BettingNet()  # adjust in_features if needed
        self.bet_model.load_state_dict(torch.load("Models\\betting_model.pth", map_location="cpu"))
        self.bet_model.eval()


        # Model output labels
        self.move_labels = ["H", "S", "D", "SP"]

    # -----------------------------------------------------------    
    # MODEL DECISION HELPERS
    # -----------------------------------------------------------    

    def ai_move(self, features):
        x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        output = self.move_model(x)
        idx = output.argmax(dim=1).item()
        return self.move_labels[idx]

    def ai_bet(self, features):
        x = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
        out = self.bet_model(x)
        return int(round(out.item()))

    # -----------------------------------------------------------    
    # MAIN PLAYER LOGIC
    # -----------------------------------------------------------    

    def place_bet(self):
        # Example features: depends on how you trained your bet model
        shoe_features = self.deck.get_csv()
        bet = self.ai_bet(shoe_features)

        # clamp to valid bet range
        bet = max(self.min_bet, min(bet, self.max_bet))

        # normalize to nearest 5
        bet = round(bet / 5) * 5

        self.hands.append(Hand(bet))
        self.total_hands += 1

    def hit_stand(self):
        hand: Hand = self.get_hand()

        # Build features for the move model
        features = [hand.get_hand_val(), self.dealer_hand.get_hand_val()] + self.deck.get_csv() + [
            int(hand.has_ace()),
            int(hand.can_split()),
            int(hand.can_double())
        ]

        move = self.ai_move(features)
        return move

    def split(self):
        current = self.hands[self.hand_index]
        split_card = current.split_hand()
        new_hand = Hand(current.get_bet())
        new_hand.append(split_card)
        self.hands.append(new_hand)

    def all_done(self):
        current = self.hands[self.hand_index]
        if current.hand_over():
            if self.hand_index + 1 == len(self.hands):
                return True
            else:
                self.hand_index += 1
                return False
        return False

    def reset(self, dealer_hand):
        dealer_val = dealer_hand.get_hand_val()

        for hand in self.hands:
            player_val = hand.get_hand_val()
            bet = hand.get_bet()

            if player_val > 21:
                self.profit -= bet
            elif dealer_val > 21:
                self.profit += bet
            else:
                if player_val > dealer_val:
                    self.profit += bet
                elif player_val < dealer_val:
                    self.profit -= bet

        self.hands = []
        self.hand_index = 0
        self.total_hands = 0

    def reset_profit(self):
        self.profit = 0

    def get_hand(self):
        return self.hands[self.hand_index]
    
    def get_profit(self):
        return self.profit
