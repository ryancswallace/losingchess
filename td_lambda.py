import parse
import losing_board
import game
import chess
import chess_agents
import evaluation
import vectorize

import random
import tensorflow as tf

class TDLeafLambda:
	def __init__(self, num_training_iterations, num_sample_positions, learning_rate, lambda_discount, num_training_turns, apply_random_move):
		# parameters of training
		self.num_training_iterations = num_training_iterations
		self.num_sample_positions = num_sample_positions
		self.learning_rate = learning_rate
		self.lambda_discount = lambda_discount
		self.num_training_turns = num_training_turns
		self.apply_random_move = apply_random_move
		
		# the weight matrix and bias vector to be calculated
		self.W = None
		self.b = None

	def train(self):
		all_training_boards = parse.pgn_to_boards('data/all_losing.pgn', labels=False, vectorized=False)
		self.vector_len = len(all_training_boards[0][0])
		# convert to losing boards
		for i, board in enumerate(all_training_boards):
			board_fen = board.fen(promoted=True)
			all_training_boards[i] = losing_board.LosingBoard(b_fen=board_fen)

			# apply random move if specified
			if self.apply_random_move:
				legal_moves = (board).get_legal_moves()
				if len(legal_moves) != 0:
					move = random.sample(legal_moves, 1)[0]
			        all_training_boards[i] = board.generate_successor(move)

		# now vectorize boards
		for i, board in enumerate(all_training_boards):
			all_training_boards[i] = vectorize.piece_vector(board)

		# holders for training board vectors
		x = tf.placeholder(tf.float32, [None, self.vector_len])

		# the weight matrix and bias vector
		W = tf.Variable(tf.zeros([self.vector_len, 1]))
		b = tf.Variable(tf.zeros([1]))

		with tf.Session() as sess:
			# initialize variables
			sess.run(tf.global_variables_initializer())

			# softmax regression to predict y
			y = tf.nn.softmax(tf.matmul(x, W) + b)

			# train using TD-learning
			# for each training iteration
			for training_iteration in range(self.num_training_iterations):
				# define evaluation functions using current weights
				eval1 = None
				eval2 = None
				
				training_boards = random.sample(all_training_boards, self.num_sample_positions)
				# for all randomly selected boards
				for training_board in training_boards:
					# play game, getting position scores
					a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=eval1, depth='1')
					a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=eval2, depth='1')

					training_game = game.Game(training_board, a1, a2)
					position_scores = training_game.play(num_training_turns)

					# calculate weight updates
					for time in range(num):
						J


			# convert evaluated tensors to np arrays
			self.W = W.eval()
			self.b = b.eval()
