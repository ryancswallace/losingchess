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
    def __init__(self, num_training_iterations, num_sample_games, learning_rate, lambda_discount, num_training_turns, apply_random_move):
        # parameters of training
        self.num_training_iterations = num_training_iterations
        self.num_sample_games = num_sample_games
        self.learning_rate = learning_rate
        self.lambda_discount = lambda_discount
        self.num_training_turns = num_training_turns
        self.apply_random_move = apply_random_move

        self.n_hidden_1 = 100
        self.n_input = self.get_input_len()
        self.x = tf.placeholder(tf.float32, [None, self.n_input])
        self.y = tf.placeholder(tf.float32, [None, 1])
        self.weights = {
            'h1': tf.Variable(tf.random_uniform([self.n_input, self.n_hidden_1])),
            'out': tf.Variable(tf.random_uniform([self.n_hidden_1, 1]))
        }
        self.biases = {
            'b1': tf.Variable(tf.random_normal([self.n_hidden_1])),
            'out': tf.Variable(tf.random_normal([1]))
        }
        
        # the weight matrix and bias vector to be calculated
        self.W = None
        self.b = None

    def nn_run(self, x, weights, biases):

        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
        layer_1 = tf.nn.relu(layer_1)
        # Hidden layer with RELU activation
        # layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
        # layer_2 = tf.nn.relu(layer_2)
        # Output layer with linear activation
        out_layer = tf.nn.tanh(tf.matmul(layer_1, weights['out'])) + biases['out']
        return out_layer

    def nn_train(self):
        all_training_boards = parse.pgn_to_boards('data/all_losing.pgn', labels=False, vectorized=False)
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
        for i, board in enumerate(all_training_boards):
            all_training_boards[i] = vectorize.piece_vector(board)

        sess = tf.InteractiveSession()
        sess.run(tf.initialize_all_variables())


        pred = self.nn_run(self.x, self.weights, self.biases)


    def train(self):
        all_training_boards = parse.pgn_to_boards('data/all_losing.pgn', labels=False, vectorized=False)
        self.vector_len = len(vectorize.piece_vector(all_training_boards[0]))
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
        for i, board in enumerate(all_training_boards):
            all_training_boards[i] = vectorize.piece_vector(board)

        # holders for training board vectors
        x = tf.placeholder(tf.float32, [None, self.vector_len])

        # the weight matrix and bias vector are initialized randomly
        W = tf.Variable(tf.random_uniform([self.vector_len, 100, 25, 1],0,0.01))
        b = tf.Variable(tf.random_uniform([1],0,0.01))

        with tf.Session() as sess:
            # initialize variables
            sess.run(tf.global_variables_initializer())

            # initialize parameters
            self.W = W.eval()
            self.b = b.eval()

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
                    print 'before play'
                    position_values, positions_vector = training_game.play(self.num_training_turns)
                    print 'after play'

                    all_positions_vectors.append(positions_vector)
                    score_changes = [0] + [position_values[i+1] - position_values[i] for i in (range(position_values) - 1)]
                    all_discounted_error_vectors.append([error * (self.lambda_discount ** t) for t, error in enumerate(score_changes)])

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
                        gradient_val = sess.run(gradient, feed_dict={x: np.array(positions_vector[time])})

                        total_error = sum(discounted_error_vector[time:(self.num_training_turns)])

                        if update_vector is None:
                            update_vector = gradient_val * total_error
                        else:
                            update_vector += gradient_val * total_error

                    # scale update vector by learning rate
                    update_vector = self.learning_rate * update_vector

                    # update weights and biases
                    self.W = map(add, self.W, update_vector)
                    self.b = map(add, self.b, update_vector)
                    print self.W
                    print self.b

    def get_input_len(self):
        all_training_boards = parse.pgn_to_boards('data/all_losing.pgn', labels=False, vectorized=False)
        return len(vectorize.piece_vector(all_training_boards[0]))



trainer = TDLeafLambda(3, 10, 0.5, 0.7, 12, False)
trainer.train()
