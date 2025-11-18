from Objects.Hand import Hand
from Objects.Card import Card
from ai_models import ModelLoader

class AIPlayer(object):
    def __init__(self, max_bet, min_bet, dealer_hand, move_model_path, bet_model_path):
        self.hand_index = 0
        self.total_hands = 0
        self.hands = []
        self.max_bet = max_bet
        self.min_bet = min_bet
        self.profit = 0
        self.dealer_hand = dealer_hand

        # Load the neural network models
        self.models = ModelLoader(move_path=move_model_path, bet_path=bet_model_path)

    # --- identical methods kept ----
    def get_proft(self): return self.profit
    def get_hand(self): return self.hands[self.hand_index]
    def reset_profit(self): self.profit = 0

    def all_done(self):
        current = self.hands[self.hand_index]
        if current.hand_over():
            if len(self.hands) == self.hand_index + 1:
                return True
            self.hand_index += 1
        return False

    def split(self):
        current = self.hands[self.hand_index]
        split_card = current.split_hand()
        new_hand = Hand(current.get_bet())
        new_hand.append(split_card)
        self.hands.append(new_hand)

    def reset(self, dealer_hand):
        dealer_val = dealer_hand.get_hand_val()
        for hand in self.hands:
            p = hand.get_hand_val()
            bet = hand.get_bet()
            if p > 21: self.profit -= bet
            elif dealer_val > 21: self.profit += bet
            else:
                if p > dealer_val: self.profit += bet
                elif p < dealer_val: self.profit -= bet

        self.hand_index = 0
        self.total_hands = 0
        self.hands = []

    # ----------------------------------------------------------
    # 1. Neural-network hit/stand/double/split
    # ----------------------------------------------------------
    def hit_stand(self):
        current = self.hands[self.hand_index]

        if current.length() == 1:
            return "C"

        player_total = current.get_hand_val()
        dealer_up = self.dealer_hand.get_hand_val()

        has_ace = 1 if current.is_soft() else 0
        can_split = 1 if current.can_split() else 0
        can_double = 1 if current.length() == 2 else 0

        # Card counts (Ace..2)
        counts = [
            self.models.shoe_counts["Ace"],
            self.models.shoe_counts["10"],
            self.models.shoe_counts["9"],
            self.models.shoe_counts["8"],
            self.models.shoe_counts["7"],
            self.models.shoe_counts["6"],
            self.models.shoe_counts["5"],
            self.models.shoe_counts["4"],
            self.models.shoe_counts["3"],
            self.models.shoe_counts["2"],
        ]

        x = self.models.format_move_input(
            player_total,
            dealer_up,
            counts,
            has_ace,
            can_split,
            can_double
        )

        with torch.no_grad():
            logits = self.models.move_model(x)
            action = torch.argmax(logits).item()

        mapping = ["H", "S", "D", "SP"]
        return mapping[action]

    # ----------------------------------------------------------
    # 2. Neural-network betting
    # ----------------------------------------------------------
    def place_bet(self):
        # Card counts only
        counts = [
            self.models.shoe_counts["Ace"],
            self.models.shoe_counts["10"],
            self.models.shoe_counts["9"],
            self.models.shoe_counts["8"],
            self.models.shoe_counts["7"],
            self.models.shoe_counts["6"],
            self.models.shoe_counts["5"],
            self.models.shoe_counts["4"],
            self.models.shoe_counts["3"],
            self.models.shoe_counts["2"],
        ]

        x = self.models.format_bet_input(counts)

        with torch.no_grad():
            out = self.models.bet_model(x)
            fraction = float(out.item())  # 0 → 1 range

        bet = self.min_bet + fraction * (self.max_bet - self.min_bet)
        bet = round(bet / 5) * 5

        self.hands.append(Hand(bet))
        self.total_hands += 1
