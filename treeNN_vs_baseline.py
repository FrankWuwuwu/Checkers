import numpy as np

from checker_helpers import *
from checker_AI import *
from TreeNN import *
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def game(game_size):
    print("player 1---baseline AI")
    print("player 2---tree+NN AI")
    state = initial_state(game_size)
    node_count=0
    while not game_over(state):

        player, board = state
        show_board(state)
        if player == 1:
            print("--- Player 1's turn --->")
            action = simple_AI(state)
            state = play_turn(action, board)
        else:
            print("--- Player 2's turn --->")
            action,node_num = treeNN_AI(state,10)
            node_count+=node_num
            state= play_turn(action, board)
    
    #player, board = state
    show_board(state)
    winner=check_winner(board)
    if winner==0:
        print("Game over, it is tied.")
    elif winner>0:
        print("Game over, player 1 wins.")
    else:
        print("Game over, player 2 wins.")
    return winner,node_count



if __name__ == "__main__":
    player1_score,player2_score = [], []
    player1_counter = 0
    player2_counter = 0
    tie_counter=0
    node_count=0
    node = []
    for i in range(100):
        print("The",i+1,"game.")
        winner,node_count=game(10)
        # player1_counter = 0
        # player2_counter = 0
        if winner>0:
            player1_counter+=1
        elif winner==0:
            tie_counter+=1
        else:
            player2_counter+=1

        player1_score.append(player1_counter)
        player2_score.append(player2_counter)
        node.append(node_count)

        print(node_count, "nodes produced by MCTS+NN")
    print("100 game finished")
    print("player 1 wins",player1_counter,"game")
    print("player 2 wins",player2_counter,"game")
    print("Tie",tie_counter,"game")

    x1 = np.linspace(1,199,100)
    x2 = np.linspace(2,200,100)
    plt.bar(x1, np.array(player1_score), label='baseline')
    plt.bar(x2, np.array(player2_score), label='tree+NN')

    # plt.xlim((1,100))

    plt.legend()

    plt.xlabel('number_game')
    plt.ylabel('score')

    plt.title('game of 10 * 10')
    plt.savefig('treeNN_experiment.jpg')
    plt.show()

    x = np.linspace(1,100,100)
    plt.bar(x, np.array(node), label='node_count')

    plt.legend()

    plt.xlabel('number_game')
    plt.ylabel('node_counts')

    plt.title('game of 10 * 10')
    plt.savefig('treeNN_experiment_node.jpg')
    plt.show()