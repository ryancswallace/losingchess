import chess
import evaluation
import chess_agents
import losing_board
import game

import copy
import numpy as np

class PieceWeightTrainer:
	"""
	A stochasic optimization method inpsired by simulated annealing that 
	tunes the piece weights used in the WeightedPieceCount evaluator.
	"""
	def __init__(self, num_init_successors=10, num_iter=10, num_subseq_successors=10, num_games=20, depth=1, starting_weights=None):
		self.num_init_successors = num_init_successors
		self.num_iter = num_iter
		self.num_subseq_successors = num_subseq_successors
		self.num_games = num_games
		self.depth = depth
		self.temp = 1
		if starting_weights == None:
			# tuned weights
			self.weights = {chess.PAWN: 2.746,
							chess.KNIGHT: 0.920,
							chess.BISHOP: 3.907,
							chess.ROOK: 3.050,
							chess.QUEEN: 6.185,
							chess.KING: 0.953}
		else:
			self.weights = starting_weights

	def perturb(self, weights):
		new_weights = copy.deepcopy(weights)
		for piece, weight in new_weights.iteritems():
			# perturb each weight by a normal amount with decreasing variance
			# as the temperature decreases
			new_weights[piece] = new_weights[piece] + np.random.normal(0, self.temp)
		return new_weights

	def train(self):
		# generate successors to the initial weights provided
		init_successors = [self.perturb(self.weights) for i in range(self.num_init_successors)] + [self.weights]
		for iteration in range(self.num_iter):
			# as we move through time, decrease the temperature
			self.temp = self.temp * 0.9
			for j, weights in enumerate(init_successors):
				# from each set of successor weights, generate subsuccessor weights
				subseq_successors = [self.perturb(weights) for i in range(self.num_subseq_successors)]
				wins = [0] * len(subseq_successors)
				for i, subseq_weights in enumerate(subseq_successors):
					# run multiple games between the successor weights and subsuccessor weights
					for trial in range(self.num_games):
						old_counter = evaluation.WeightedPieceCount(weights)
						new_counter = evaluation.WeightedPieceCount(subseq_weights)

						old_agent = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=old_counter.evaluate, depth=self.depth, ant_eval_func=new_counter.evaluate, parallelize=True)
						new_agent = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=new_counter.evaluate, depth=self.depth, ant_eval_func=old_counter.evaluate, parallelize=True)
						board = losing_board.LosingBoard(no_kings=False)

						g = game.Game(board, old_agent, new_agent, get_stats=True)
						winner = g.play(max_turns=200)

						if winner == chess.WHITE:
							wins[i] -= 1
						elif winner == chess.BLACK:
							wins[i] += 1

				# update the successor weights to the best subsuccessor weights
				init_successors[j] = subseq_successors[wins.index(max(wins))]

		# for all the updated successor weights, choose the best set by single elimination
		candidate1 = init_successors[0]
		for i in range(len(init_successors) - 1):
			candidate2 = init_successors[i+1]

			old_counter = evaluation.WeightedPieceCount(candidate1)
			new_counter = evaluation.WeightedPieceCount(candidate2)

			old_agent = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=old_counter.evaluate, depth=self.depth, ant_eval_func=new_counter.evaluate, parallelize=True)
			new_agent = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=new_counter.evaluate, depth=self.depth, ant_eval_func=old_counter.evaluate, parallelize=True)
			board = losing_board.LosingBoard(no_kings=False)

			g = game.Game(board, old_agent, new_agent, get_stats=True)
			winner = g.play(max_turns=200)

			if winner == chess.WHITE or winner == None:
				candidate1 = candidate1 
			elif winner == chess.BLACK:
				candidate1 = candidate2

		# the final tuned weights
		self.weights = candidate1
		return self.weights

trainer = PieceWeightTrainer(num_init_successors=6, num_iter=10, num_subseq_successors=8, num_games=8, depth=1, starting_weights=None)
print trainer.train()		

