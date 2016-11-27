import chess.pgn
import vectorize

"""
Given a .pgn file, returns a list of chess.pgn.Game objects
representing the games.
"""
def pgn_to_games(pgn_file):
	pgn = open(pgn_file)
	games = []
	while True:
		try:
			game = chess.pgn.read_game(pgn)
		except ValueError:
			print 'Error parsing. Continuing.'
			break
		
		if game == None:
			# end of pgn file
			break
		else:
			games.append(game)

	return games

def pgn_to_labeled_board(pgn_file):
	games = pgn_to_games(pgn_file)
	board_result_pairs = []
	for game in games:
		# get result of game - 0 for draw, 1 for white win, 2 for black win
		result_string = game.headers['Result']
		result = None
		if result_string == '1/2-1/2':
			result = 0
		elif result_string == '1-0':
			result = 1
		elif result_string == '0-1':
			result = 2
		else:
			continue

		# move through all boards seen in game (except initial configuration)
		node = game
		while not node.is_end():
			node = node.variation(0)
			vector = vectorize.piece_vector(node.board())
			board_result_pairs.append((vector, result))

# board_result_pairs = pgn_to_labeled_board('data/all_losing.pgn')
