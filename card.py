class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self.get_value()
    
    def get_value(self):
        if self.rank == '0':
            return 0
        elif self.rank == 'A':
            return 1
        elif self.rank in ['J', 'Q', 'K']:
            return 10
        else:
            return int(self.rank)

    def __repr__(self):
        return f"{self.rank}{self.suit}"
