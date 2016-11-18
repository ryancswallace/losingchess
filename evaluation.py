import chess

"""
Here we'll put our evaluation functions
"""

# I made these up
naive_weights = {chess.PAWN: 1,
				 chess.KING: 2,
				 chess.KNIGHT: 3,
				 chess.BISHOP: 3,
				 chess.ROOK: 3,
				 chess.QUEEN: 4}

WEIGHTS_SUM = 33


def weighted_piece_count(game_state, color):
	
	pieces = game_state.piece_counts[not color]

	tot = WEIGHTS_SUM
	for k in pieces:
		tot -= pieces[k]*naive_weights[k]

	return tot