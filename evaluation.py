import chess
import tensorflow as tf
import numpy as np

"""
Here we'll put our evaluation functions
"""

# approximate piece values
naive_weights = {chess.PAWN: 1,
                 chess.KING: 2,
                 chess.KNIGHT: 3,
                 chess.BISHOP: 5,
                 chess.ROOK: 3,
                 chess.QUEEN: 6}

class Evaluator:
    def evaluate(self, game_state, color):
        raise Exception("Undefined!")

class WeightedPieceCount(Evaluator):
    def evaluate(self, game_state, color):
        pieces = game_state.piece_counts

        tot = 0
        for k in pieces[color]:
            tot -= pieces[color][k]*naive_weights[k]

        return tot

class AntiPawn(Evaluator):
    def evaluate(self, game_state, color):
        return -game_state.piece_counts[color][chess.PAWN]

class WeightedPieceCountWCaptures(Evaluator):
    def captures_present(self, game_state, color):
        # for all legal moves
        legal_moves = game_state.get_legal_moves()
        for mv in legal_moves:
            # check if any move captures
            if game_state.board.piece_at(mv.to_square):
                return True
        return False

    def evaluate(self, game_state, color):        
        weighted_piece_counter = WeightedPieceCount()
        if self.captures_present(game_state, color):
            return weighted_piece_counter.evaluate(game_state, color) - 5
        else:
            return weighted_piece_counter.evaluate(game_state, color) + 5

class SoftmaxEval(Evaluator):
    def __init__(self, softmax_model):
        self.softmax_model = softmax_model
        if self.softmax_model.W is None or self.softmax_model.b is None:
            raise Exception('Train softmax first.')

        # tensor for board_vector
        self.x = tf.placeholder(tf.float32, [1, self.softmax_model.vector_len])

        # the weight matrix and bias vector
        W = tf.constant(self.softmax_model.W, dtype=tf.float32)
        b = tf.constant(self.softmax_model.b, dtype=tf.float32)

        self.sess = tf.InteractiveSession()
        
        # initialize variables
        self.sess.run(tf.global_variables_initializer())

        # define model with weights and biases calculated
        self.y = tf.nn.softmax(tf.matmul(self.x, W) + b)

    def evaluate(self, game_state, color):
        board_vector = self.softmax_model.vectorize_method(game_state.board)

        # predict new board
        predict = tf.argmax(self.y,1)
        x_np = np.array(board_vector).reshape(1,len(board_vector))
        pred = self.sess.run(predict, feed_dict={self.x: x_np})[0]
        if color == chess.WHITE:
            return pred
        else:
            return 2 - pred

class MultilayerEval(Evaluator):
    def __init__(self, multilayer_model):
        self.multilayer_model = multilayer_model
        if self.multilayer_model.W is None or self.multilayer_model.b is None:
            raise Exception('Train multilayer first.')

        # tensor for board_vector
        self.x = tf.placeholder(tf.float32, [1, self.multilayer_model.n_input])

        self.sess = tf.InteractiveSession()
        
        # initialize variables
        self.sess.run(tf.global_variables_initializer())

        # define model with weights and biases calculated
        self.y = multilayer_model.multilayer_perceptron(self.x, self.multilayer_model.W, self.multilayer_model.b)

    def evaluate(self, game_state, color):
        board_vector = self.multilayer_model.vectorize_method(game_state.board)

        # score new board
        score = self.y
        x_np = np.array(board_vector).reshape(1,len(board_vector))
        preds = self.sess.run(score, feed_dict={self.x: x_np})[0]
    
        if color == chess.WHITE:
            print preds[2] - preds[0]
            return preds[2] - preds[0]
        else:
            print preds[0] - preds[2]
            return preds[0] - preds[2]

class TDTrainEval(Evaluator):
    def __init__(self, model):
        self.model = model
        if self.model.W is None or self.model.b is None:
            raise Exception('Initialize/train model first.')

        # tensor for board_vector
        self.x = tf.placeholder(tf.float32, [1, self.model.vector_len])

        # the weight matrix and bias vector
        W = tf.constant(self.model.W, dtype=tf.float32)
        b = tf.constant(self.model.b, dtype=tf.float32)

        self.sess = tf.InteractiveSession()
        
        # initialize variables
        self.sess.run(tf.global_variables_initializer())

        # define model with weights and biases calculated
        self.y = tf.nn.softmax(tf.matmul(self.x, W) + b)

    def evaluate(self, game_state, color):
        board_vector = self.model.vectorize_method(game_state.board)

        # predict new board
        predict = tf.argmax(self.y,1)
        x_np = np.array(board_vector).reshape(1,len(board_vector))
        pred = self.sess.run(predict, feed_dict={self.x: x_np})[0]

        if color == chess.WHITE:
            return pred
        else:
            return 1 - pred
 