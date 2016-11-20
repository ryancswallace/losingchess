import chess

"""
Here we'll put our evaluation functions
"""

# I made these up
naive_weights = {chess.PAWN: 1,
				 chess.KING: -9999,
				 chess.KNIGHT: 3,
				 chess.BISHOP: 3,
				 chess.ROOK: 3,
				 chess.QUEEN: 4}

def weighted_piece_count(game_state, color):
	
	pieces = game_state.piece_counts

	tot = 0
	for k in pieces[color]:
		tot += (pieces[color][k] - pieces[not color][k])*naive_weights[k]

	return tot

def anti_pawn(game_state, color):

	return -game_state.piece_counts[color][chess.PAWN]