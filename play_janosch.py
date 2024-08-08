import random
import argparse

from tqdm import tqdm

from janosch import JanoschGame

OG4 = ['Enno', 'Dani', 'Caro', 'Mariia']

def main(play_rounds=1, silent='no'):
    silent_dict = {'yes': True, 'no': False}

    score_board = {roommate: 0 for roommate in OG4}
    
    for i in tqdm(range(play_rounds)):
        random.shuffle(OG4)
        
        player_names = OG4[:2]          # play two v two
        agents = player_names                     # no agents

        game = JanoschGame(player_names, agents, silent=silent_dict[silent])

        loser = game.start_game()
        score_board[loser] += 1

    print(score_board)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Play Janosch game.')
    parser.add_argument('-r', '--rounds', type=int, default=1, help='Number of rounds to play')
    parser.add_argument('-s', '--silent', type=str, default='no', help='Whether to report the game state')

    args = parser.parse_args()

    main(args.rounds, args.silent)
