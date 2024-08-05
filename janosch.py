import random
from typing import List, Optional
from card import Card
from deck import Deck
from player import Player


JANOSCH_THRESHOLD = 15

class JanoschGame:
    def __init__(self, player_names: List[str], agents: List[str], silent):
        self.players = [Player(name, name not in agents) for name in player_names]
        self.current_player_index = 0
        self.janosch_called = False
        self.janosch_caller: Optional[Player] = None
        self.deck = None
        self.discard_pile = []
        self.silent = silent
        self.initialize_game()
    
    def initialize_game(self):
        self.deck = Deck()
        random.shuffle(self.deck.cards)
        self.discard_pile = [self.deck.draw_card()]
        self.deal_cards()

    def deal_cards(self):
        for player in self.players:
            player.draw_hand(self.deck)
        self.discard_pile.append(self.deck.draw_card())
    
    def play_turn(self, player_index: int):
        player = self.players[player_index]
        if not self.silent: print()
        if not self.silent: print(player)
        # self.print_hand(player)

        if player.is_human:
            if not self.janosch_called:
                action = input("Janosch? Y/N: ").strip().upper()
                if action == "Y":
                    self.call_janosch(player)
                    return

            self.play_card_action(player)
            self.draw_card_action(player)
        else:
            if not self.janosch_called and player.calculate_hand_value() <= JANOSCH_THRESHOLD:
                self.call_janosch(player)
                return

            self.agent_play_card_action(player)
            self.agent_draw_card_action(player)

    def print_hand(self, player: Player):
        if not self.silent: print(f"{player.name}'s hand:")
        for i, card in enumerate(player.hand):
            if not self.silent: print(f"{i + 1}: {card}")

    def play_card_action(self, player: Player):
        discard_ix = int(input("Enter the index of the card to discard: ").strip()) - 1
        card = self.find_card_in_hand(player, discard_ix)

        if card:
            player.play_card(card)
            self.discard_pile.append(card)
            if not self.silent: print(f"Discarded {card}")
        else:
            if not self.silent: print("Card not found in hand.")

        if self.deck.is_empty():
            if not self.silent: print("Deck is empty. Reshuffling discard pile.")
            self.deck.cards = self.discard_pile[:]
            self.discard_pile = []
            self.deck.shuffle()

    def agent_play_card_action(self, player: Player):

        if self.deck.is_empty():
            if not self.silent: print("Deck is empty. Reshuffling discard pile.")
            self.deck.cards = self.discard_pile[:]
            random.shuffle(self.deck.cards)
            self.discard_pile = [self.deck.draw_card()]

        card = player.discard_highest_card()
        self.discard_pile.append(card)
        if not self.silent: print(f"{player.name} (Agent) discarded {card}")

        
    def draw_card_action(self, player: Player):
        draw_action = input(f'Draw {self.discard_pile[-2]} (1) or random (2)?: ').strip()
        if draw_action == '1':
            drawn_card = self.discard_pile.pop()
        elif draw_action == '2':
            drawn_card = self.deck.draw_card()
        else:
            if not self.silent: print('Invalid input')
            return

        player.add_card(drawn_card)
        if not self.silent: print(f"Drew {drawn_card}")

    def agent_draw_card_action(self, player: Player):
        if player.should_draw_from_discard_pile(self.discard_pile):
            drawn_card = self.discard_pile.pop(-2)
            if not self.silent: print(f"{player.name} (Agent) drew {drawn_card} from discard pile")
        else:
            drawn_card = self.deck.draw_card()
            if not self.silent: print(f"{player.name} (Agent) drew {drawn_card} from deck")
        
        player.add_card(drawn_card)
    
    def find_card_in_hand(self, player: Player, discard_ix: int) -> Optional[Card]:
        if 0 <= discard_ix < len(player.hand):
            return player.hand[discard_ix]
        return None
    
    def call_janosch(self, player: Player):
        if player.calculate_hand_value() <= JANOSCH_THRESHOLD:
            self.janosch_called = True
            if not self.silent: print(f"{player.name} called Janosch!")
            self.janosch_caller = player
        else:
            if not self.silent: print("Janosch call invalid.")
    
    def end_round(self):
        if self.janosch_caller:
            janosch_caller_score = self.janosch_caller.calculate_hand_value()
            other_players_scores = [player.calculate_hand_value() for player in self.players if player != self.janosch_caller]

            if janosch_caller_score > min(other_players_scores):
                self.janosch_caller.score += 30 + janosch_caller_score
                if not self.silent: print(f"{self.janosch_caller.name} called Janosch but didn't have the lowest hand. They receive a penalty.")
            else:
                if not self.silent: print(f"{self.janosch_caller.name} called Janosch and won the round!")

            for player in self.players:
                if player != self.janosch_caller:
                    player.score += player.calculate_hand_value()
                    if not self.silent: print(f"{player.name} receives {player.calculate_hand_value()} points.")

            self.janosch_called = False
            self.janosch_caller = None

            for player in self.players:
                if player.score >= 100:
                    if not self.silent: print(f"{player.name} has reached or exceeded 100 points and loses the game!")
                    if not self.silent: print(self)
                    return player.name

        return None
    
    def start_game(self):
        while True:
            self.initialize_game()

            while not self.janosch_called:
                self.play_turn(self.current_player_index)
                self.current_player_index = (self.current_player_index + 1) % len(self.players)

                if self.current_player_index == 0:
                    if not self.silent: print(self)
                
            if not self.silent: print("Janosch called, proceeding with final turns for other players.")

            for _ in range(len(self.players)):
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                if self.players[self.current_player_index] != self.janosch_caller:
                    self.play_turn(self.current_player_index)

            loser = self.end_round()
            if loser:
                return loser
   
    def __repr__(self):
        game_state = "\n# # ## # # # ## # # # # ## # # ## # "
        game_state += "\nJanoschGame State:\n"
        for player in self.players:
            hand = ', '.join(str(card) for card in player.hand)
            game_state += f"{player.name} - Hand: [{hand}], Score: {player.score}\n"
        game_state += "# # ## # # # ## # # # # ## # # ## # \n"
        
        return game_state[:-2]

