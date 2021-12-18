####code by Kefu Wu
import numpy as np
from checker_helpers import *
from checker_AI import *

class Node:
        def __init__(self, all_data):
            # tree_player is the player of this tree
            # player is the player that make move at current state
            (tree_player,state)=all_data
            self.tree_player=tree_player
            self.player, self.board = state
            self.visit_count = 0
            self.score_total = 0
            self.score_estimate = 0
            self.child_list = []
            
        def children(self):
            if self.child_list == []:
                new_child=[]
                state= (self.player, self.board)
                all_action = valid_actions(state)
                #print(all_action)
                for action in all_action:
                    #print(action)
                    new_state=simu_turn(action,self.board)
                    #show_board(new_state)
                    new_child.append((self.tree_player,new_state))
                    self.child_list = list(map(Node, new_child))
            return self.child_list
            
        def N_values(self):
            return [c.visit_count for c in self.children()]
            
        def Q_values(self):
            children = self.children()
            sign = +1 if self.player == self.tree_player else -1
            Q = [sign * c.score_total / (c.visit_count+1) for c in children]
            # Q = [sign * c.score_total / max(c.visit_count, 1) for c in children]
            return Q


def exploit(node):
    return node.children()[np.argmax(node.Q_values())]

def explore(node):
    return node.children()[np.argmin(node.N_values())] # TODO

def uct(node):
    # max_c Qc + sqrt(ln(Np) / Nc)
    Q = np.array(node.Q_values())
    N = np.array(node.N_values())
    U = Q + np.sqrt( np.log(node.visit_count + 1) / (N + 1))
    #print(node.children())
    return node.children()[np.argmax(U)]
    

# choose_child = exploit
# choose_child = explore
choose_child = uct

# decide the best action of current node base on UCT
def decide_action(node):
    Q = np.array(node.Q_values())
    N = np.array(node.N_values())
    U = Q + np.sqrt( np.log(node.visit_count + 1) / (N + 1))
    state= (node.player, node.board)
    all_action = valid_actions(state)
    return all_action[np.argmax(U)]


def rollout(node):
    if game_over((node.player, node.board)):
        if node.tree_player==1:
            result_sign=1
        elif node.tree_player ==2:
            result_sign=-1
        else:
            print("player error")
        result = result_sign*check_winner(node.board)
    else: result = rollout(choose_child(node))
    node.visit_count += 1
    node.score_total += result
    node.score_estimate = node.score_total / node.visit_count
    return result
    
def get_action(node):
    make_move=decide_action(node)
    
    #print(make_move)   
    action_type, start, end= make_move
    if action_type==0:
        type_text="move"
    if action_type==1:
        type_text="jump"
    print ("treebased AI action:",type_text,"the checker of",start,"to",end)
    
    return make_move

def MCTS_AI(state,rolltime):
    tree_player, board =state
    # gauge sub-optimality with rollouts
    node = Node((tree_player,(tree_player,board)))
    for r in range(rolltime): 
        rollout(node)
        #print(r, node.score_estimate)
    #print("choice")
    #print(node.tree_player)
    
    return get_action(node), checknode(node)

def node_tree(state,rolltime):
    tree_player, board =state
    node = Node((tree_player,(tree_player,board)))
    for r in range(rolltime): 
        rollout(node)
        print("rollout time:",r)
    
    return node

def checknode(node):
    num=len(node.child_list)
    for item in node.child_list:
        num+=checknode(item)
    return num

if __name__ == "__main__":


    tree_player, board =initial_state(14)
    # gauge sub-optimality with rollouts
    node = Node((tree_player,(tree_player,board)))
    for r in range(500): # TODO
        rollout(node)
        print(r, node.score_estimate)
    print("choice")
    show_board((tree_player, board))
    get_action(node)