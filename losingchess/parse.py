import chess.pgn
import os

def pgn_to_games(pgn_file):
    """
    Given a .pgn file, returns a list of chess.pgn.Game objects
    representing the games.
    """
    pgn = open(pgn_file)
    print 'This following is fine (expected behavior):'
    games = []
    while True:
        try:
            game = chess.pgn.read_game(pgn, chess.pgn.GameModelCreator)
        except ValueError:
            print 'Error parsing. Continuing.'
            break

        if game == None:
            # end of pgn file
            break
        else:
            games.append(game)

    return games


def pgn_to_boards(num_data_sets, labels=False, vectorize_method=None):
    """
    Using pgn_to_games, returns a list of boards occurring in the games data.
    num_data_sets should be <= 9, and .pgns must be in data directory.
    """
    num_data_sets = min(num_data_sets, 9)

    pgn_files = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, 'data')
    pgn_file_names = ['all_losing_' + str(i) + '.pgn' for i in range(num_data_sets)]
    for pgn_file_name in pgn_file_names:
        pgn_files.append(os.path.join(dir_path, pgn_file_name))
    
    games = []
    for pgn_file in pgn_files:
        games += pgn_to_games(pgn_file)
    
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
            if vectorize_method is None:
                if labels:
                    board_result_pairs.append((node.board(), result))
                else:
                    board_result_pairs.append(node.board())
            else:
                vector = vectorize_method(node.board())
                if labels:
                    board_result_pairs.append((vector, result))
                else:
                    board_result_pairs.append(vector)
                

    return board_result_pairs
