####code by Kefu Wu 580824208 11/30/2021

import numpy as np
import matplotlib.pyplot as pt

def initial_state(board_size) -> tuple:
    # player 1 and player 2, 0 means empty, -1 means not-reachable spot
    # 3 means king checker of player 1
    # 4 means king checker of player 2
    player=1
    if (board_size<=4):
        board_size=6
        print("The minimal board size is 6! new board size: ", board_size,"*",board_size)
    
    if (board_size%2)>0:
        board_size+=1
        print("board size must be even! new board size: ", board_size,"*",board_size)
    
    # init board
    num_rows, num_cols = board_size, board_size
    board = 0*np.ones((num_rows, num_cols), dtype=int)
    
    # put not reachable spot
    for x in range(board_size):
        for y in range(board_size):
            if (x%2>0)!=(y%2>0):
                board[x,y]=-1
                
    for y in range(board_size):
        for x in range(board_size):
            if x<=((board_size/2) -2):
                if board[x,y]!=-1:
                    board[x,y]=2
            if x>=((board_size/2) +1):
                if board[x,y]!=-1:
                    board[x,y]=1
    return (player, board)


# if no action can be performed, the game over
def game_over(state: tuple) -> bool: 
    return (valid_actions(state) ==[])


def valid_actions(state: tuple) -> list:
    (player, board)=state
    valid=[]
    # form (action,(start),(end)) 
    # action 0: normal move
    # action 1: jump
    avaliable_checkers=[]
    avaliable_kings=[]
    jump=[]
    board_size=len(board)
    for x in range(board_size):
        for y in range(board_size):
            if board[x,y]==player:
                avaliable_checkers.append((x,y))
            if board[x,y]==player+2:
                avaliable_kings.append((x,y))
    for checkers in avaliable_checkers:
        r,c = checkers
        if (player==1):
            rival=2
            if r-1>=0 and c-1>=0:
                if board[r-1,c-1]==0:
                    valid.append((0,(r,c),(r-1,c-1)))
                # check jump
                if board[r-1,c-1]==rival:
                    if r-2>=0 and c-2>=0:
                        if board[r-2,c-2]==0:
                            jump.append((1,(r,c),(r-2,c-2)))
            if r-1>=0 and c+1<=board_size-1:
                if board[r-1,c+1]==0:
                    valid.append((0,(r,c),(r-1,c+1)))
                # check jump
                if board[r-1,c+1]==rival:
                    if r-2>=0 and c+2<=board_size-1:
                        if board[r-2,c+2]==0:
                            jump.append((1,(r,c),(r-2,c+2)))
        if (player==2):
            rival=1
            if r+1<=board_size-1 and c-1>=0:
                if board[r+1,c-1]==0:
                    valid.append((0,(r,c),(r+1,c-1)))
                # check jump
                if board[r+1,c-1]==rival:
                    if r+2<=board_size-1 and c-2>=0:
                        if board[r+2,c-2]==0:
                            jump.append((1,(r,c),(r+2,c-2)))
            if r+1<=board_size-1 and c+1<=board_size-1:
                if board[r+1,c+1]==0:
                    valid.append((0,(r,c),(r+1,c+1)))
                # check jump
                if board[r+1,c+1]==rival:
                    if r+2<=board_size-1 and c+2<=board_size-1:
                        if board[r+2,c+2]==0:
                            jump.append((1,(r,c),(r+2,c+2)))
    
    
    # if player can jump, he/she must jump
    if jump==[]:
        return valid
    else:
        return jump
        

def play_turn(move: tuple, board: list) -> tuple:
    action, start, end= move
    
    # check who is moving
    player=board[start]
    if (player==1):
        rival=2
    if (player==2):
        rival=1
    
    if action==0:
        board[start]=0
        board[end]=player
        return (rival,board)
    if action==1:
        board[start]=0
        board[end]=player
        xs, ys = start
        xe, ye = end
        board[int((xs+xe)/2),int((ys+ye)/2)]=0
        state= player, board
        valid=valid_actions(state)
        jump=[]
        for item in valid:
            new_action, new_start, new_end= item
            if new_action==1:
                jump.append(item)
        #print(valid)
        #print(jump)
        if jump==[]:
            return (rival,board)
        else:
            return (player,board)

def check_winner(board):
    player1_count=0
    player2_count=0
    board_size=len(board)
    for x in range(board_size):
        for y in range(board_size):
            if board[x,y]==1 or board[x,y]==3:
                player1_count+=1
            if board[x,y]==2 or board[x,y]==4:
                player2_count+=1
    if (player1_count==player2_count):
        return 0
    if player1_count>player2_count:
        return 1
    else:
        return 2


# show the whole board to user
def show_board(state):
    player, board=state
    board_size=len(board)
    process_list=range(board_size)
    #if player==2:
    #    process_list=reversed(range(board_size))
    for x in process_list:
        str_row=""
        for y in process_list:
            current_box=str(board[x,y])
            if current_box=="-1":
                current_box="X"
            if current_box=="0":
                current_box="-"
            str_row+=current_box
            str_row+=" "
        print(str_row)

