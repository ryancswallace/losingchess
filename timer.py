import game
import chess
import chess_agents
import evaluation
import losing_board

import numpy as np
import time
import seaborn as sns
import pandas as pd

counter = evaluation.WeightedPieceCount()

print '### MINIMAX ###'
for depth in [0, 1, 2]:
    print 'DEPTH ', depth
    times = []
    for i in range(10): 
        a1 = chess_agents.MinimaxAgent(color=chess.WHITE, eval_func=counter.evaluate, depth=depth, ant_eval_func=counter.evaluate)
        a2 = chess_agents.MinimaxAgent(color=chess.BLACK, eval_func=counter.evaluate, depth=depth, ant_eval_func=counter.evaluate)
        board = losing_board.LosingBoard(no_kings=False)

        game_to_play = game.Game(board, a1, a2)

        start = time.time()
        game_to_play.play()
        end = time.time()
        times.append(end - start)
        print (end - start)

        if depth == 2 and i > 3:
            break

    print 'MINIMAX DEPTH ' + str(depth) + ': ' + str(np.mean(times))

print '### A-B NO PARALLELIZATION ###'
for depth in [0, 1, 2]:
    print 'DEPTH ', depth
    times = []
    for i in range(10):
        a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=counter.evaluate, depth=depth, ant_eval_func=counter.evaluate)
        a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=counter.evaluate, depth=depth, ant_eval_func=counter.evaluate)
        board = losing_board.LosingBoard(no_kings=False)

        game_to_play = game.Game(board, a1, a2)

        start = time.time()
        game_to_play.play()
        end = time.time()
        times.append(end - start)
        print (end - start)

        if depth == 2 and i > 3:
            break

    print 'A-B NO PARALLELIZATION ' + str(depth) + ': ' + str(np.mean(times))

print '### A-B WITH PARALLELIZATION ###'
for depth in [0, 1, 2]:
    print 'DEPTH ', depth
    times = []
    for i in range(10):
        a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=counter.evaluate, depth=depth, ant_eval_func=counter.evaluate, parallelize=True)
        a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=counter.evaluate, depth=depth, ant_eval_func=counter.evaluate, parallelize=True)
        board = losing_board.LosingBoard(no_kings=False)

        game_to_play = game.Game(board, a1, a2)

        start = time.time()
        game_to_play.play()
        end = time.time()
        times.append(end - start)
        print (end - start)
        
        if depth == 2 and i > 3:
            break

    print 'A-B WITH PARALLELIZATION ' + str(depth) + ': ' + str(np.mean(times))

times = pd.Series([0.446, 40.201, 9150.533, 0.417, 10.635, 432.256, 0.417, 7.518, 109.635], name='Time')
depths = pd.Series([1,2,3,1,2,3,1,2,3], name='Depth')
methods = pd.Series(['Minimax', 'Minimax', 'Minimax', 'Alpha-Beta', 'Alpha-Beta', 'Alpha-Beta', 'Alpha-Beta w/ Parallelization', 'Alpha-Beta w/ Parallelization', 'Alpha-Beta w/ Parallelization'], name='Search_Method')

times_df = pd.concat([times, depths, methods], axis=1)

ax = sns.barplot(x="Search_Method", y="Time", hue="Depth", data=times_df)
ax.set(xlabel='Search Method', ylabel='Average Game Duration in Seconds (log scale)')
ax.set_yscale('log')
sns.plt.show()

