import chess

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
	def weighted_piece_count(self, game_state, color):
	    pieces = game_state.piece_counts

	    tot = 0
	    for k in pieces[color]:
	        tot += (pieces[color][k] - pieces[not color][k])*naive_weights[k]

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

    def softmax_eval(self, game_state, color):
    	board_vector = vectorize.piece_vector(game_state.board)
    	if color == chess.WHITE:
    		return self.softmax_model.eval(board_vector)
    	else:
    		return 1 - self.softmax_model.eval(board_vector)
