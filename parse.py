import chess.pgn

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
