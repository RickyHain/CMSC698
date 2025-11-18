import torch
import torch.nn as nn
import torch.nn.functional as F

# ----------------------------
# Model definitions
# ----------------------------
class MoveNet(nn.Module):
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

class BetNet(nn.Module):
    def __init__(self, in_features=10, hidden1=64, hidden2=32, out_features=1):
        super().__init__()
        self.fc1 = nn.Linear(in_features, hidden1)
        self.fc2 = nn.Linear(hidden1, hidden2)
        self.fc3 = nn.Linear(hidden2, out_features)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return torch.relu(self.fc3(x))


# ----------------------------
# Loader wrapper
# ----------------------------
class ModelLoader:
    def __init__(self, move_path=None, bet_path=None):
        self.move_model = None
        self.bet_model = None

        if move_path:
            self.move_model = MoveNet()
            self.move_model.load_state_dict(torch.load(move_path, map_location="cpu"))
            self.move_model.eval()

        if bet_path:
            self.bet_model = BetNet()
            self.bet_model.load_state_dict(torch.load(bet_path, map_location="cpu"))
            self.bet_model.eval()

    # Format movement input for MoveNet
    def format_move_input(self, player, dealer, counts, has_ace, can_split, can_double):
        total = sum(counts)
        norm_counts = [c / total for c in counts]
        x = [
            player / 21,
            dealer / 11,
            *norm_counts,
            has_ace,
            can_split,
            can_double
        ]
        return torch.tensor(x, dtype=torch.float32)

    # Format input for BetNet
    def format_bet_input(self, counts):
        total = sum(counts)
        norm_counts = [c / total for c in counts]
        return torch.tensor(norm_counts, dtype=torch.float32)
