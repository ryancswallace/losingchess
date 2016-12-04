import game
import chess
import chess_agents
import evaluation
import losing_board
import sys
import StringIO
from copy import deepcopy

class StatsGenerator:

	def compare_agents(self, a1, a2, board, n_iter, verbose=False):

		a1_victory_dict = {chess.WHITE:[], chess.BLACK:[]}

		for a in [a1, a2]:
			print "One agent with " + a.eval_func.im_func.func_name + " and search depth " + str(a.depth)

		for i in range(n_iter/2):
			tmp_board = deepcopy(board)
			g1 = game.Game(tmp_board, a1, a2, get_stats=True)
			a1_victory, move_cnt = g1.play(verbose=verbose, max_turns=200)
			a1_victory_dict[chess.WHITE].append((a1_victory, move_cnt))

		for i in range(n_iter/2):
			tmp_board = deepcopy(board)
			g2 = game.Game(tmp_board, a2, a1, get_stats=True)
			a1_victory, move_cnt = g2.play(verbose=verbose, max_turns=200)
			a1_victory_dict[chess.BLACK].append((not a1_victory, move_cnt) if a1_victory is not None else (None, move_cnt))

		return a1_victory_dict


def get_win_proc(l):
	results = zip(*l)[0] 
	wins = [w for w in results if w is not None]
	return sum(wins)/float(len(results)), (len(wins) - sum(wins))/float(len(results))


if __name__ == "__main__":

	alternate_weights = {chess.PAWN: 6,
						chess.KING: 5,
						chess.KNIGHT: 3,
						chess.BISHOP: 3,
						chess.ROOK: 2,
						chess.QUEEN: 1}

	anti_pawn = evaluation.AntiPawn()
	counter1 = evaluation.WeightedPieceCount()
	counter2 = evaluation.WeightedPieceCount(weights=alternate_weights)

	a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=counter1.weighted_piece_count, depth='1')
	a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=counter2.weighted_piece_count, depth='1')
	board = losing_board.LosingBoard(no_kings=False)

	s = StatsGenerator()
	out_dict = s.compare_agents(a1, a2, board, 40)

		