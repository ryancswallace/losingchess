import chess
import tensorflow as tf
import numpy as np
import vectorize

"""
Here we'll put our evaluation functions
"""

# I made these up
naive_weights = {chess.PAWN: 1,
                 chess.KING: 2,
                 chess.KNIGHT: 3,
                 chess.BISHOP: 5,
                 chess.ROOK: 3,
                 chess.QUEEN: 6}

class WeightedPieceCount:
    def __init__(self, weights=naive_weights):
        self.weights = weights

    def weighted_piece_count(self, game_state, color):
        pieces = game_state.piece_counts

        tot = 0
        for k in pieces[color]:
            tot -= pieces[color][k]*self.weights[k]

        return tot

class AntiPawn:
    def anti_pawn(self, game_state, color):
        return -game_state.piece_counts[color][chess.PAWN]

class WeightedPieceCountWCaptures:
    def captures_present(self, game_state, color):
        # for all pieces
        pieces = game_state.piece_counts
        for piece in pieces[color]:
            # look at all moves
            legal_moves = game_state.get_legal_moves()
            for mv in legal_moves:
                # check if any move captures
                if game_state.board.piece_at(mv.to_square):
                    return True
        return False

    def weighted_piece_count_w_captures(self, game_state, color):        
        weighted_piece_counter = WeightedPieceCount()
        if self.captures_present(game_state, color):
            return weighted_piece_counter.weighted_piece_count(game_state, color) - 5
        else:
            return weighted_piece_counter.weighted_piece_count(game_state, color) + 5

class SoftmaxEval:
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


    def softmax_eval(self, game_state, color):
        board_vector = vectorize.piece_vector(game_state.board)
        print game_state.board

        # predict new board
        predict = tf.argmax(self.y,1)
        x_np = np.array(board_vector).reshape(1,len(board_vector))
        pred = self.sess.run(predict, feed_dict={self.x: x_np})[0]
        print pred
        if color == chess.WHITE:
            return pred
        else:
            return 2 - pred
