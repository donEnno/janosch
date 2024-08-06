import random
from card import Card

class Deck:
    def __init__(self):
        suits = ['H', 'D', 'C', 'S']
        ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 0]
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks[:-1]] + [Card('0', 0)] * 2  # Add two jokers
        random.shuffle(self.cards)
    
    def draw_card(self):
        return self.cards.pop()
    
    def is_empty(self):
        return len(self.cards) == 0
