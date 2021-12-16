from checker_helpers import *
from checker_AI import *

class Node:
        def __init__(self, player, board):
            self.board = board
            self.player = player 
            self.visit_count = 0
            self.score_total = 0
            self.score_estimate = 0
            self.child_list = None
            
        def children(self):
                if self.child_list == None:
                    state= (player, board)
                    all_action = valid_actions(state)
                    
                    #self.child_list = list(map(Node, (action,board)))
                return self.child_list
