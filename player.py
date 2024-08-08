from typing import List
from card import Card
from deck import Deck

class Player:
    def __init__(self, name: str, is_human: bool = True):
        self.name = name
        self.hand: List[Card] = []
        self.score: int = 0
        self.is_human = is_human
    
    def draw_hand(self, deck: Deck):
        self.hand = [deck.draw_card() for _ in range(5)]
    
    def play_card(self, card: Card):
        self.hand.remove(card)
    
    def add_card(self, card: Card):
        self.hand.append(card)
    
    def calculate_hand_value(self) -> int:
        return sum(card.value for card in self.hand)
    
    def __repr__(self) -> str:
        # sorted hand by value
        return f"{self.name} - Hand: {self.hand}, Score: {self.score}"


class Agent(Player):
    def __init__(self, name: str):
        super().__init__(name, is_human=False)

    def discard_highest_card(self) -> Card:
        highest_card = max(self.hand, key=lambda card: card.value)
        self.play_card(highest_card)
        return highest_card

    def should_draw_from_discard_pile(self, discard_pile: List[Card]) -> bool:
        if not discard_pile:
            return False
        highest_card_value = max(self.hand, key=lambda card: card.value).value
        return discard_pile[-2].value < highest_card_value
    
    def find_best_move(self) -> List[Card]:
        best_move = []
        lowest_value_after_move = self.calculate_hand_value()

        # Evaluate single card discard
        for card in self.hand:
            value_after_move = self.calculate_hand_value() - card.value
            if value_after_move < lowest_value_after_move:
                lowest_value_after_move = value_after_move
                best_move = [card]
        print(best_move)
        
        # Evaluate sets (groups of cards with the same rank)
        for rank in set(card.rank for card in self.hand):
            set_of_cards = [card for card in self.hand if card.rank == rank]
            if len(set_of_cards) > 1:
                value_after_move = self.calculate_hand_value() - sum(card.value for card in set_of_cards)
                if value_after_move < lowest_value_after_move:
                    lowest_value_after_move = value_after_move
                    best_move = set_of_cards
        print(best_move)
        # Evaluate straights (consecutive cards of the same suit)
        suits = set(card.suit for card in self.hand)
        for suit in suits:
            sorted_hand = sorted([card for card in self.hand if card.suit == suit], key=lambda c: c.rank)
            for i in range(len(sorted_hand) - 2):
                straight = sorted_hand[i:i + 3]
                if len(straight) == 3 and (straight[2].rank - straight[1].rank == 1) and (straight[1].rank - straight[0].rank == 1):  # Check for consecutive ranks
                    value_after_move = self.calculate_hand_value() - sum(card.value for card in straight)
                    if value_after_move < lowest_value_after_move:
                        lowest_value_after_move = value_after_move
                        best_move = straight
        print(best_move)
        input()
        return best_move

    def play_best_move(self) -> List[Card]:
        best_move = self.find_best_move()
        for card in best_move:
            self.play_card(card)
        return best_move
