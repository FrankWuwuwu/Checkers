from checker_helpers import *
from checker_AI import *
from MCTS import *

def game(game_size):
    print("player 1---baseline AI")
    print("player 2---treebased AI")
    state = initial_state(game_size)
    
    while not game_over(state):

        player, board = state
        show_board(state)
        if player == 1:
            print("--- Player 1's turn --->")
            action = simple_AI(state)
            state = play_turn(action, board)
        else:
            print("--- Player 2's turn --->")
            action = MCTS_AI(state,500)
            
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
    return winner



if __name__ == "__main__":

    # get game size
    while True:
        try:
            question = int(input('Please enter an integer for the board size(e.g 8 for 8*8 game):'))
            if question<30:
                break
            else:
                print("board size larger than 30*30 is not supported.")
                continue
        except:
            print("Invalid input, please enter an integer!")
    
    player1_counter=0
    player2_counter=0
    tie_counter=0
    for i in range(100):
        print("The",i+1,"game.")
        winner=game(question)
        if winner>0:
            player1_counter+=1
        elif winner==0:
            tie_counter+=1
        else:
            player2_counter+=1
    print("100 game finished")
    print("player 1 wins",player1_counter,"game")
    print("player 2 wins",player2_counter,"game")
    print("Tie",tie_counter,"game")
