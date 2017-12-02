import game
import chess
import chess_agents
import evaluation
import losing_board
import softmax
import vectorize
import sys
import StringIO
import random
from copy import deepcopy
from scipy.stats import binom

unif_weights = {chess.PAWN: 1,
                 chess.KING: 1,
                 chess.KNIGHT: 1,
                 chess.BISHOP: 1,
                 chess.ROOK: 1,
                 chess.QUEEN: 1}

class WeightTuner:

	def __init__(self, init_weights=unif_weights, max_iter=100, depth=1):
		self.max_iter = max_iter
		self.depth = depth
		self.weights = init_weights

	def tune(self):

		for i in range(self.max_iter):
			c1 = evaluation.WeightedPieceCount(weights=self.weights)
			new_weights = deepcopy(self.weights)
			c2 = evaluation.WeightedPieceCount(weights=self._jiggle_weights(new_weights))

			a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=c1.evaluate, depth=1, ant_eval_func=c2.evaluate)
			a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=c2.evaluate, depth=1, ant_eval_func=c1.evaluate)

			order = [(a1, c1), (a2, c2)]
			random.shuffle(order)

			board = losing_board.LosingBoard()

			g = game.Game(board, order[0][0], order[1][0], get_stats=True)

			winner = g.play()

			if winner:
				self.weights = order[0][1].weights
			else:
				self.weights = order[1][1].weights

		return weights


	def _jiggle_weights(self, weights):

		print weights

		random_key = random.choice(weights.keys())
		random_change = random.choice([-.5, .5])

		weights[random_key] += random_change

		return weights


if __name__ == "__main__":

	c = WeightTuner()
	c.tune()
