import numpy as np
import random
from checker_helpers import *



def simple_AI(state):
    action=random.choice(valid_actions(state))
    print("AI action:",action)
    return action



