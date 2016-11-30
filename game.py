import sys
import chess
import losing_board
import chess_agents
import evaluation
import time

"""
Here we will build the processes that drive games between two AIs,
and games between an AI and a human.

Perhaps we'll use command line arguments to select agent types,
evaluation functions, number of AIs, a la Berkeley.
"""

def run_game(a1, a2, no_kings=True):
	board = losing_board.LosingBoard(no_kings=no_kings)
	for i in range(1000):

		outer_break = False
		turn = False
		for agent in [a1,a2]:
			mv = agent.get_move(board)
			if not mv:
				outer_break = True
				print "It's a draw."
				break
			board.move(mv)

			print "Agent " + str(turn + 1) + " makes move: "+ str(mv)
			print board
			print

			turn = not turn

			if board.is_game_over():
				print 
				print "Agent " + str(turn + 1) + " victorious in " + str(board.board.fullmove_number) + " plies."
				print
				return turn + 1
				outer_break = True
				break
			if board.is_draw():
				print "It's a draw in " + str(board.board.fullmove_number) + " plies."
				print
				draw = True
				break
		
		if outer_break: break

from functools import partial

def get_stats(ag1, ag2, runs, verbose=False):

	if not verbose:
		save_stdout = sys.stdout
		sys.stdout = open('trash', 'w')

	run_this_game = partial(run_game, a1=ag1, a2=ag2, no_kings=True)

	#p = Pool(8)
	wins = [run_this_game() for i in range(runs)]
	#p.terminate

	if not verbose:
		sys.stdout = save_stdout

	return wins


if __name__ == '__main__':
	a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=evaluation.anti_pawn, depth='1')
	a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=evaluation.weighted_piece_count, depth='1')
	print get_stats(a1, a2, 10)




	
