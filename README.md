# Introduction
This is the Group project of CIS 667 AI class.

Group members:  Kefu Wu,  Shuangding Zhu,  Jiayu Ding

We are implementing checkers with a rule modification and train AI for the game.

We use **MTCS** and **CNN** to train AI for this project.

**Rule modification: each turn, there is a 10% chance that a player's piece automatically teleports to a random nearby location. This will always happen after the player makes their move.**

We implement three kind of AI for this game:

Baseline AI -- choose an action uniformly at random

tree-based AI -- implemented by MTCS and use UCT as strategy for children selection. 

tree+NN AI -- use trained CNN to produce utility for states. Integrated into MTCS to prioritize children selection.

# Required libraries
To run our game, following libraries must be installed.
```
matplotlib
numpy
pytorch
```
You can find how to install numpy here:
https://numpy.org/install/

You can find how to install matplotlib here:
https://matplotlib.org/3.4.3/users/installing.html

You can find how to install pytorch here:
https://pytorch.org/get-started/locally/


# How to run the game
The code of the game is created by us and is completely original.
To start with, use following code to clone and enter the project.
```
git clone https://github.com/FrankWuwuwu/Checkers
cd Checkers
```
run following code to play checker with simple AI.
```
python play_checker.py
```

Once started, you will be able to choose the game size and the control for two players.

We provide 4 kind of control.

1. Human

2. Baseline AI

4. tree-based AI

6. tree+NN AI

Play with AI and enjoy the game.

# How to run experiment

We present two kind of experiment to evaluate the performance of our AI.

Run following script will execute 100 game between **baseline AI and tree-based AI** with 500 rollout for MCTS.
```
python tree_vs_baseline.py
```
Two graph will be produced after the execution of result. One records the distribution of game score, one records the number of node produced by tree-based AI.
In this script, we set the board size to be 6*6. You can edit the board size and rollout in the code for further experiment.

Run following script will execute 100 game between **baseline AI and tree+NN AI** with 10 rollout for MCTS.
```
python treeNN_vs_baseline.py
```
Two graph will also produced by this script.
In this script, we set the board size to be 10*10. You can edit the board size and rollout in the code for further experiment.

# Other files

MCTS.py -- code of tree-based AI

TreeNN.py -- code of CNN integrated tree AI

data_generator.py -- method to generate training data for our neural network

CNN_version1/2/3.py -- code of three kind of CNN configuration we tried. **Input: 1*8*8 array of game states. Output: utilities**

checker_AI.py -- code of baseline AI
