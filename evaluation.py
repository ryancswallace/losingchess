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
		tot -= (pieces[color][k] - pieces[not color][k])*naive_weights[k]

	return tot

def anti_pawn(game_state, color):

	return -game_state.piece_counts[color][chess.PAWN]


def captures_present(game_state, color):
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

def weighted_piece_count_w_captures(game_state, color):
	if captures_present(game_state, color):
		return weighted_piece_count(game_state, color) - 5
	else:
		return weighted_piece_count(game_state, color) + 5