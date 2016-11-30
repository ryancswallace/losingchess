import chess
import losing_board
import random
import time
from functools import partial
from multiprocessing import Pool

class Agent:

    def __init__(self, eval_func, color=chess.WHITE, depth='1'):
        self.color = color
        self.eval_func = eval_func
        self.depth = int(depth)

    def get_move(self, game_state):
        raise Exception("Undefined!")


class RandomAgent(Agent):
	def get_move(self, game_state):
		moves = game_state.get_legal_moves()
		move = random.sample(moves, 1)[0]
		return move


class UserAgent(Agent):
	def get_move(self, game_state):
		while True:
			inmv = raw_input("Enter your move: ")
			mv = chess.Move.from_uci(inmv)
			if mv in game_state.get_legal_moves():
				return mv


def _alpha_beta_value(move, game_state, alpha, beta, depth, color, true_color, true_depth, eval_func):
	"""
	Helper function for performing alpha-beta pruning in parallel.
	"""
	# has max depth been reached?
	if depth == true_depth:
		return eval_func(game_state, color)

	# get next game state
	next_state = game_state.generate_successor(move)

	# has agent won?
	if next_state.is_game_over():
		return 99999

	# does agent move next?
	next_color = not color

	# get information about next state
	next_moves = next_state.get_legal_moves()

	# if this agent is to move
	if next_color == true_color:

		# increment depth if agent is pacman
		depth += 1

		# if we've reached a terminal state
		# update alpha and return terminal value
		if next_moves == []:
			term_val = eval_func(next_state, next_color)
			alpha = max(alpha, term_val)
			return term_val

		# find next action with max utility
		v = -99999
		for mv in next_moves:
			mvValue = _alpha_beta_value(mv, next_state, alpha, beta, depth, next_color, true_color, true_depth, eval_func)
			v = max(v, mvValue)
			# prune if value is great enough
		if v > beta:
		  return v
		alpha = max(alpha, v)
		return v

	# if opponent is to move
	else:
		# if we've reached a terminal state
		# return terminal value without updating alpha/beta
		if next_moves == []:
			term_val = eval_func(next_state, next_color)
			return term_val

		# find next action with min utility
		v = 99999
		for mv in next_moves:
			mvValue = _alpha_beta_value(mv, next_state, alpha, beta, depth, next_color, true_color, true_depth, eval_func)
			v = min(v, mvValue)
			#prune if value is small enough
			if v < alpha:
				return v
			beta = min(beta, v)
		return v

<<<<<<< HEAD
	def get_move(self, game_state):
		"""
		Return minimax move using self.depth, self.eval_func, and alpha-beta pruning.
		"""

		moves = game_state.get_legal_moves()

		if len(moves) == 0:
			return None


		get_ab_value = partial(_alpha_beta_value, game_state=game_state, 
								alpha=-99999, beta=99999, depth=0, 
								color=self.color, true_color=self.color, 
								true_depth=self.depth, eval_func=self.eval_func)

		p = Pool(8)
		values = p.map(get_ab_value, moves)
		p.terminate()

		val_dict = {mv: v for mv, v in zip(moves, values)}

		# return action with max utility, 
		# random action if there's a tie
		best_val = max(val_dict.values())	
		best_actions = []
		for k, v in val_dict.iteritems():
			if v == best_val:
				best_actions.append(k)

		return random.sample(best_actions, 1)[0]



	def _alpha_beta_value(self, move, game_state, alpha, beta, depth, color):
		"""
		Helper function for performing alpha-beta pruning.
		"""
		# has max depth been reached?
		if depth == self.depth:
			return self.eval_func(game_state, color)

		# get next game state
		next_state = game_state.generate_successor(move)

		# has agent won?
		if next_state.is_game_over():
			return 99999

		# does agent move next?
		next_color = not color

		# get information about next state
		next_moves = next_state.get_legal_moves()

		# if this agent is to move
		if next_color == self.color:

			# increment depth if agent is pacman
			depth += 1

			# if we've reached a terminal state
			# update alpha and return terminal value
			if next_moves == []:
				term_val = self.eval_func(next_state, next_color)
				alpha = max(alpha, term_val)
				return term_val

			# find next action with max utility
			v = -99999
			for mv in next_moves:
				mvValue = self._alpha_beta_value(mv, next_state, alpha, beta, depth, next_color)
				v = max(v, mvValue)
				# prune if value is great enough
			if v > beta:
			  return v
			alpha = max(alpha, v)
			return v

		# if opponent is to move
		else:
			# if we've reached a terminal state
			# return terminal value without updating alpha/beta
			if next_moves == []:
				term_val = self.eval_func(next_state, next_color)
				return term_val

			# find next action with min utility
			v = 99999
			for mv in next_moves:
				mvValue = self._alpha_beta_value(mv, next_state, alpha, beta, depth, next_color)
				v = min(v, mvValue)
				#prune if value is small enough
				if v < alpha:
					return v
				beta = min(beta, v)
			return v
