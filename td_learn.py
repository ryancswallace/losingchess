import parse
import losing_board
import game
import chess
import chess_agents
import evaluation

import random
import tensorflow as tf

all_training_boards = parse.pgn_to_boards('data/all_losing.pgn')
vector_len = len(board_result_pairs[0][0])

# x = tf.placeholder(tf.float32, [None, 784])
# W = tf.Variable(tf.zeros([vector_len, 3]))
# b = tf.Variable(tf.zeros([3]))
# y = tf.nn.softmax(tf.matmul(x, W) + b)

# parameters of training
num_training_iterations = 10
num_sample_positions = 256
num_training_turns = 12
apply_random_move = False

all_training_boards = parse.pgn_to_boards('data/all_losing.pgn', labels=False, vectorized=False)
# convert to losing boards
for i, board in enumerate(all_training_boards):
	board_fen = board.fen(promoted=True)
	all_training_boards[i] = losing_board.LosingBoard(b_fen=board_fen)

	# apply random move if specified
	if apply_random_move:
		legal_moves = (all_training_boards[i]).get_legal_moves()
		if len(legal_moves) != 0:
			move = random.sample(legal_moves, 1)[0]
	        all_training_boards[i] = (all_training_boards[i]).generate_successor(move)

# train using TD-learning
for training_iteration in range(num_training_iterations):
	training_boards = random.sample(all_training_boards, num_sample_positions)
	for training_board in training_boards:
		a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=evaluation.weighted_piece_count, depth='1')
		a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=evaluation.weighted_piece_count, depth='1')
		training_game = game.Game(training_board, a1, a2)
		position_scores = training_game.play(num_training_turns)
		