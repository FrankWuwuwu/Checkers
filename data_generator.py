import numpy as np
import random

from checker_helpers import *
from checker_AI import *
from MCTS import *

def get_child(node,board_list,utility_list):
    if node.visit_count<6 or len(utility_list)>=1000:
        return
    board_list.append(node.board)
    utility_list.append(node.score_estimate)
    if node.child_list==[]:
        return
    for children in node.child_list:
        get_child(children,board_list,utility_list)


def get_traing_data():
    state = initial_state(10)
    
    board_list=[]
    utility_list=[]
    
    node=node_tree(state,10000)
    get_child(node,board_list,utility_list)
    
    # board_list, 10*10 list, need to change to 1*10*10
    print(len(board_list))
    # utility_list, the corresponding utility
    print(len(utility_list))
    
    # check if the data set is normal case, should be a float number between -10~10. 
    print(sum(utility_list)/ len(utility_list))
    return board_list, utility_list
        
        
    

