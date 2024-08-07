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
