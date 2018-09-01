# ticTacToe_v2
Learning project to create working minimalistic tic tac toe game

## Usage

From the project directory, play 10 games on  a 3x3 board with GUI and minimax bot as "O" by running:
```python
python ticTacToe.py -d 3 --score 3 --bot_o minimax --display gui --num_games 10
```

## About the current bots

Currently, 3 different bots are implemented:

1. A random bot ("random") (always plays random move).
2. A minimax bot ("minimax") plays according to minimax algorithm with alpha-beta pruning. Plays 3x3 board optimally, for bigger board sizes uses some (very simple) heuristics to choose moves. Does not fall to really obvious pitfalls, but does not play a strong game either.
3. A Monte Carlo Tree Search ("mcts") bot. Uses UCT criteria for selection step, and random rollout policy for simulation step. Plays currently quite bad. One reason is the poor rollout policy.
