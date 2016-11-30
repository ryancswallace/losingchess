import chess.pgn
import vectorize

"""
Given a .pgn file, returns a list of chess.pgn.Game objects
representing the games.
"""
def pgn_to_games(pgn_file):
    pgn = open(pgn_file)
    games = []
    # while True:
    for _ in range(100):
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

def pgn_to_boards(pgn_file, labels=False, vectorized=False):
    games = pgn_to_games(pgn_file)
    board_result_pairs = []
    for game in games:
        # get result of game - 0.5 for draw, 1 for white win, 0 for white loss
        result_string = game.headers['Result']
        result = None
        if result_string == '1/2-1/2':
            result = 0.5
        elif result_string == '1-0':
            result = 1
        elif result_string == '0-1':
            result = 0
        else:
            continue

        # move through all boards seen in game (except initial configuration)
        node = game
        while not node.is_end():
            node = node.variation(0)
            if vectorized:
                vector = vectorize.piece_vector(node.board())
                if labels:
                    board_result_pairs.append((vector, result))
                else:
                    board_result_pairs.append(vector)
            else:
                if labels:
                    board_result_pairs.append((node.board(), result))
                else:
                    board_result_pairs.append(node.board())

    return board_result_pairs
