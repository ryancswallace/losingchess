import parse
import losing_board
import game
import chess
import chess_agents
import evaluation
import vectorize

import random
import numpy as np
import tensorflow as tf
from operator import add


class TDLeafLambda:
    def __init__(self, num_training_iterations, num_sample_games, num_data_sets, learning_rate, lambda_discount, num_training_turns, apply_random_move, vectorize_method):
        # parameters of training
        self.num_training_iterations = num_training_iterations
        self.num_sample_games = num_sample_games
        self.num_data_sets = num_data_sets
        self.learning_rate = learning_rate
        self.lambda_discount = lambda_discount
        self.num_training_turns = num_training_turns
        self.apply_random_move = apply_random_move
        self.vectorize_method = vectorize_method
        self.vector_len = vectorize.get_vector_len(vectorize_method)

        # the weight matrix and bias vector to be calculated
        self.W = None
        self.b = None

    def train(self):
        all_training_boards = parse.pgn_to_boards(self.num_data_sets, labels=False, vectorize_method=None)

        # convert to losing boards
        for i, board in enumerate(all_training_boards):
            board_fen = board.fen()
            all_training_boards[i] = losing_board.LosingBoard(b_fen=board_fen)

            # apply random move if specified
            if self.apply_random_move:
                legal_moves = (all_training_boards[i]).get_legal_moves()
                if len(legal_moves) != 0:
                    move = random.sample(legal_moves, 1)[0]
                    all_training_boards[i] = (all_training_boards[i]).generate_successor(move)

        # now vectorize boards
        all_vectorized_training_boards = []
        for i, board in enumerate(all_training_boards):
            all_vectorized_training_boards.append(self.vectorize_method(board))

        # check vector length
        assert self.vector_len == len(all_vectorized_training_boards[0])

        # holders for training board vectors
        x = tf.placeholder(tf.float32, [None, self.vector_len])

        # the weight matrix and bias vector are initialized randomly
        W = tf.Variable(tf.random_uniform([self.vector_len, 1], 0, 0.01))
        b = tf.Variable(tf.random_uniform([1], 0, 0.01))

        sess = tf.InteractiveSession()
        # initialize variables
        sess.run(tf.global_variables_initializer())

        # initialize parameters
        self.W = W.eval()
        self.b = b.eval()

        sess.close()

        # define evaluation functions using current weights
        current_evaluator = evaluation.TDTrainEval(self)
        evaluator = current_evaluator.eval

        # train using TD-learning
        # for each training iteration
        for training_iteration in range(self.num_training_iterations):
            training_boards = random.sample(all_training_boards, self.num_sample_games)
            all_discounted_error_vectors = []
            all_positions_vectors = []

            # for all randomly selected boards
            for training_board in training_boards:
                # play game, getting position scores
                a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=evaluator, depth='1')
                a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=evaluator, depth='1')

                training_game = game.Game(training_board, a1, a2)
                position_values, positions_vector = training_game.play(self.num_training_turns)

                all_positions_vectors.append(positions_vector)
                score_changes = [0] + [position_values[i + 1] - position_values[i] for i in
                                       range(len(position_values) - 1)]
                all_discounted_error_vectors.append(
                    [error * (self.lambda_discount ** t) for t, error in enumerate(score_changes)])

            for i in range(self.num_sample_games):
                # get list of position vectors and discounted errors for this game
                positions_vector = all_positions_vectors[i]
                discounted_error_vector = all_discounted_error_vectors[i]
                update_vector = None
                # for each time frame in the game
                for time in range(self.num_training_turns):
                    # calculate the gradient of the L1 loss function with respect to 
                    # connection weights and biases of the neural network
                    gradient = tf.gradients(evaluator, [x])

                    sess = tf.InteractiveSession()
                    gradient_val = sess.run(gradient, feed_dict={x: np.array(positions_vector[time])})

                    total_error = sum(discounted_error_vector[time:(self.num_training_turns)])

                    if update_vector is None:
                        update_vector = gradient_val * total_error
                    else:
                        update_vector += gradient_val * total_error

                    sess.close()

                # scale update vector by learning rate
                update_vector = self.learning_rate * update_vector

                # update weights and biases
                self.W = map(add, self.W, update_vector)
                self.b = map(add, self.b, update_vector)
                print self.W
                print self.b
