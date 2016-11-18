import chess
import losing_board
import random

class Agent:

	def __init__(self, eval_func, color=chess.WHITE, depth='1'):
		self.color = color
		self.eval_func = eval_func
		self.depth = int(depth)

	def getMove(self, gameState):
		raise Exception("Undefined!")


class RandomAgent(Agent):
	def getMove(self, gameState):
		moves = gameState.getLegalMoves()
		move = random.sample(moves, 1)[0]
		return move


############### DOES NOT WORK AND IS UGLY! ####################
class AlphaBetaAgent(Agent):

	def getMove(self, gameState):
		"""
		Return minimax move using self.depth, self.eval_func, and alpha-beta pruning.
		"""

		moves = gameState.getLegalMoves()

		p = .1		# with probability p, choose random action
		if random.uniform(0,1) < p:
			return random.sample(moves, 1)[0]

		values = {}
		alpha = -99999
		for move in moves:
			values[move] = self._alpha_beta_value(move, gameState, -99999, 99999, 0, self.color)
			alpha = max(alpha, values[move])

		# return action with max utility
		try:
			return max(values, key=lambda v: v[1])[0]	
		except:
			print moves, values


	def _alpha_beta_value(self, move, gameState, alpha, beta, depth, color):
		"""
		Helper function for performing alpha-beta pruning.
		"""
		# has max depth been reached?
		if depth == self.depth:
			return self.eval_func(gameState, color)

		# get next game state
		nextState = gameState.generateSuccessor(move)

		# has agent won?
		if nextState.isGameOver():
			return 99999

		# does agent move next?
		next_color = not color

		# get information about next state
		nextMoves = nextState.getLegalMoves()

		# if this agent is to move
		if next_color == self.color:

			# increment depth if agent is pacman
			depth += 1

			# if we've reached a terminal state
			# update alpha and return terminal value
			if nextMoves == []:
				termVal = self.eval_func(nextState, next_color)
				alpha = max(alpha, termVal)
				return termVal

			# find next action with max utility
			v = -99999
			for mv in nextMoves:
				mvValue = self._alpha_beta_value(mv, nextState, alpha, beta, depth, next_color)
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
			if nextMoves == []:
				termVal = self.eval_func(nextState, next_color)
				return termVal

			# find next action with min utility
			v = 99999
			for mv in nextMoves:
				mvValue = self._alpha_beta_value(mv, nextState, alpha, beta, depth, next_color)
				v = min(v, mvValue)
				#prune if value is small enough
				if v < alpha:
					return v
				beta = min(beta, v)
			return v

