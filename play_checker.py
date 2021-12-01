from checker_helpers import *
from checker_AI import *

def get_user_action(state):
    actions = valid_actions(state)
    player, board = state
    print( "Player %d, choose an action (enter the index): " % (player))
    for index,action in enumerate(actions):
        action_type, start, end= action
        if action_type==0:
            type_text="move"
        if action_type==1:
            type_text="jump"
        print (index,"  ", type_text,"the checker of",start,"to",end)
    while True:
        try:
            choice = int(input("Your action:"))
        except:
            print("Invalid input, please enter an integer of index.")
            continue
        if choice in range(len(actions)): return tuple(actions[int(choice)])
        print("Invalid action, try again.")

if __name__ == "__main__":

    state = initial_state(4)
    while not game_over(state):

        player, board = state
        show_board(state)
        if player == 1:
            action = get_user_action(state)
            state = play_turn(action, board)
        else:
            print("--- AI's turn --->")
            action = simple_AI(state)
            state= play_turn(action, board)
    
    #player, board = state
    show_board(state)
    winner=check_winner(board)
    if winner==0:
        print("Game over, it is tied.")
    else:
        print("Game over, player %d wins." % winner)

