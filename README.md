# Janosch

I will have you Asaf'd!

## About This Project

**Janosch** is a Python implementation of a card game similar to Rummy or Gin Rummy. The game is designed for 2+ players and involves strategic card play with the goal of achieving the lowest hand value.

## Game Overview

Janosch is a competitive card game where players:
- Draw and discard cards to minimize their hand value
- Form sets (cards of the same rank) and straights (consecutive cards of the same suit)
- Call "Janosch" when their hand value is 5 or less to end the round
- Accumulate penalty points based on their remaining hand value
- The first player to reach 100 points **loses** the game

### Game Mechanics

#### Card Values
- **Aces (A)**: 1 point
- **Number cards (2-10)**: Face value
- **Face cards (J, Q, K)**: 10 points each
- **Jokers (0)**: 0 points (wildcards)

#### Deck Composition
- Standard 52-card deck (4 suits: Hearts, Diamonds, Clubs, Spades)
- 2 Jokers (wildcards)
- Total: 54 cards

#### Gameplay
1. **Initial Deal**: Each player receives 5 cards
2. **Turn Structure**:
   - **Discard Phase**: Play a single card, a set (2+ cards of same rank), or a straight (3+ consecutive cards of same suit)
   - **Draw Phase**: Draw from the discard pile or the deck
3. **Calling Janosch**: When a player's hand value ≤ 5, they can call "Janosch" to trigger the final round
4. **Scoring**: After Janosch is called, remaining players take one final turn, then scores are calculated:
   - If the Janosch caller has the lowest hand: They score 0, others score their hand value
   - If the Janosch caller doesn't have the lowest hand: They receive a 30-point penalty + their hand value
5. **Game End**: First player to reach 100 points loses

### Valid Moves
- **Single Card**: Discard any single card
- **Set**: 2 or more cards of the same rank (e.g., three 7s)
- **Straight**: 3 or more consecutive cards of the same suit (e.g., 5♥, 6♥, 7♥)
- Jokers can be used in sets and straights as wildcards

## Project Structure

```
janosch/
├── card.py           # Card class with suit, rank, and value
├── deck.py           # Deck class managing the card collection
├── player.py         # Player and Agent classes
├── janosch.py        # Main game logic and rules
├── play_janosch.py   # Game runner script for simulations
└── README.md         # This file
```

## Key Components

### Classes

#### `Card` (card.py)
Represents a single playing card with:
- `suit`: Card suit (H, D, C, S, or 0 for Jokers)
- `rank`: Card rank (1-13, or 0 for Jokers)
- `value`: Point value for scoring

#### `Deck` (deck.py)
Manages the card deck:
- Initializes a 54-card deck (52 cards + 2 jokers)
- Supports drawing cards
- Tracks when the deck is empty

#### `Player` (player.py)
Represents a human player with:
- Hand management (drawing, playing, adding cards)
- Score tracking
- Hand value calculation

#### `Agent` (player.py)
AI player that extends Player:
- `find_best_move()`: Evaluates all possible moves to minimize hand value
- `play_best_move()`: Executes the optimal move
- `should_draw_from_discard_pile()`: Strategic decision-making for drawing cards

#### `JanoschGame` (janosch.py)
Core game engine managing:
- Game state (players, deck, discard pile, scores)
- Turn management
- Move validation (sets, straights)
- Janosch calling mechanics
- Round end conditions and scoring

## Usage

### Running the Game

#### Interactive Play (Human Players)
```bash
python play_janosch.py
```

#### Simulations (AI vs AI)
```bash
# Run 100 silent games to collect statistics
python play_janosch.py -r 100 -s yes

# Run 10 games with verbose output
python play_janosch.py -r 10 -s no
```

### Command-Line Arguments
- `-r, --rounds`: Number of rounds to play (default: 1)
- `-s, --silent`: Whether to suppress game state output ('yes' or 'no', default: 'no')

### Game Configuration
Edit `play_janosch.py` to customize:
- `OG4`: List of player names (default: ['Enno', 'Dani', 'Caro', 'Mariia'])
- `player_names`: Number of active players (default: 2)
- `agents`: Which players are AI-controlled

## Features

### Human Players
- Interactive command-line gameplay
- Real-time hand display
- Move validation with helpful error messages
- Strategic decision-making for calling Janosch

### AI Agents
- Intelligent move evaluation considering:
  - Single card discards
  - Set formations
  - Straight formations
- Optimal hand value minimization
- Strategic card drawing from discard pile
- Automatic Janosch calling when hand value ≤ 5

### Game Simulation
- Batch game execution with progress tracking (tqdm)
- Statistical scoreboard tracking losses across multiple games
- Silent mode for performance testing

## Strategy Tips

1. **Minimize High-Value Cards**: Face cards (J, Q, K) are worth 10 points each
2. **Form Sets and Straights**: Discard multiple cards at once to reduce hand value quickly
3. **Time Your Janosch Call**: Call when you're confident you have the lowest hand
4. **Watch the Discard Pile**: Strategic drawing can help complete sets or straights
5. **Use Jokers Wisely**: Jokers (0 points) are valuable wildcards for completing combinations

## Development

The codebase is organized with clear separation of concerns:
- **Models**: Card, Deck, Player classes
- **Game Logic**: JanoschGame orchestration
- **AI**: Agent decision-making algorithms
- **CLI**: play_janosch.py runner script

## Future Enhancements

Potential areas for expansion:
- Web-based UI for online multiplayer
- Advanced AI strategies (Monte Carlo simulations, reinforcement learning)
- Tournament mode with brackets
- Statistics tracking and visualization
- Custom rule variants
- Network multiplayer support

---

**Note**: The phrase "I will have you Asaf'd!" appears to be an inside joke or reference related to the game's origins.
