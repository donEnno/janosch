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
        self.current_action = None
        self.last_action = 'start'
        self.initialize_game()
    
    def initialize_game(self):
        self.deck = Deck()
        random.shuffle(self.deck.cards)
        self.discard_pile = [self.deck.draw_card()]
        self.deal_cards()

    def deal_cards(self):
        for player in self.players:
            player.draw_hand(self.deck)
    
    def is_set(self, cards):
        if len(cards) < 2:
            return False

        # remove jokers
        cards_wo_joker = [card for card in cards if card.rank != 0]


        if all(card.rank == cards[0].rank for card in cards_wo_joker):
            self.current_action = ('set', len(cards))
            return True
        else:
            return False
            
    def is_straight(self, cards):

        if len(cards) < 3:
            return False

        # False when not all cards have the same suit
        if not all(card.suit == cards[0].suit for card in cards):
            return False

        jokers = [card for card in cards if card.rank == 0]
        non_jokers = [card for card in cards if card.rank != 0]

        sorted_cards = sorted(non_jokers, key=lambda card: card.rank)
        
        gaps = 0
        for i in range(len(sorted_cards) - 1):
            gap = sorted_cards[i + 1].rank - sorted_cards[i].rank - 1
            gaps += gap
            print(gap, gaps)
        
        if gaps <= len(jokers):
            self.current_action = ('straight', len(cards))
            return True
        
        return False


    def play_turn(self, player_index: int):
        player = self.players[player_index]
        player.hand = sorted(player.hand, key=lambda card: card.rank)

        if not self.silent: print()
        if not self.silent: print(player)
        # self.print_hand(player)

        if player.is_human:
            if not self.janosch_called:
                action = input("Janosch? y/n: ").strip()
                if action == "y":
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
        discard_ixs = input("Enter indices of the cards to discard like 1 2 3: ").strip().split()
        discard_ixs = [int(ix) - 1 for ix in discard_ixs]

        selected_cards = [self.find_card_in_hand(player, ix) for ix in discard_ixs]

        if len(selected_cards) == 1 or self.is_set(selected_cards) or self.is_straight(selected_cards):
            
            if self.is_straight(selected_cards):
                selected_cards = sorted(selected_cards, key=lambda card: card.rank)
            
            if len(selected_cards) == 1:
                self.current_action = ('single', 1)

            for card in selected_cards:
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
        current_ix = self.current_action[1]

        if self.last_action == 'start':
            available_cards = [self.discard_pile[-current_ix-1]]
        else:    
            last_ix = self.last_action[1]
            available_cards = self.discard_pile[-last_ix-current_ix:-current_ix]

        self.last_action = self.current_action
        
        if len(available_cards) == 1:
            draw_action = input(f'Draw {self.discard_pile[-current_ix-1]} (1) or random (2)?: ').strip()
            if draw_action == '1':
                drawn_card = self.discard_pile.pop(-2)
            elif draw_action == '2':
                drawn_card = self.deck.draw_card()
            else:
                if not self.silent: print('Invalid input')
                return

        if len(available_cards) > 1:
            draw_action = input(f'Draw one of {available_cards[0]} or {available_cards[-1]} (1 / 2) or random (3)?: ').strip()

            if draw_action == '1':
                self.discard_pile.remove(available_cards[0])
                drawn_card = available_cards[0]
            elif draw_action == '2':
                self.discard_pile.remove(available_cards[-1])
                drawn_card = available_cards[-1]
            elif draw_action == '3':
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

