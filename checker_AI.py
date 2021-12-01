import numpy as np
import random
from checker_helpers import *



def simple_AI(state):
    action=random.choice(valid_actions(state))
    action_type, start, end= action
    if action_type==0:
        type_text="move"
    if action_type==1:
        type_text="jump"
    print ("AI action:",type_text,"the checker of",start,"to",end)
    return action



