import chess
from copy import deepcopy

class LosingBoard:
    """
    Wrapper for the python-chess Board class that encodes the rules of losing chess
    (a.k.a. anti-chess, suicide chess).

    The dynamics of the game are the same as regular chess. The rules are different.

    The rules:
    -> First player to lose all pieces wins.
    -> Attacking pieces must capture opponent's piece.
    -> Pawns are automatically promoted to Queens.
    """

    def __init__(self, no_kings=False, b_fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        k=1
        self.no_kings = no_kings
        if self.no_kings:
            self.board = chess.Board(fen='rnbq1bnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQ1BNR w Qq - 0 1')
            k=0
        else:
            self.board = chess.Board(fen=b_fen)

        self.piece_counts = { color: {
                                        chess.PAWN: 8,
                                        chess.ROOK: 2,
                                        chess.BISHOP: 2,
                                        chess.QUEEN: 1,
                                        chess.KING: k,
                                        chess.KNIGHT: 2,
                                    }

                             for color in [chess.WHITE, chess.BLACK]
                            }


    def get_legal_moves(self):
        """
        Return list of all legal moves for a color given the current gamestate.
        Since the Board class knows whose turn it is, we need not take a color argument.
        """

        legal_moves = []

        # TODO castling shouldn't actually be allowed
        # get pseudo legal moves under normal chess rules (includes putting king into check)
        chess_legal_moves = self.board.pseudo_legal_moves

        # check for attacking positions
        # if one is found, we only include attacking moves among legal moves
        attacking = False
        for mv in chess_legal_moves:
            if self.board.piece_at(mv.to_square):
                legal_moves.append(mv)
                attacking = True

        if attacking:
            return legal_moves
        else:
            return list(chess_legal_moves)


    def move(self, mv):
        """
        Push move mv to true board.
        """

        p = self.board.piece_at(mv.to_square)

        # decrement count of pieces if one is captured
        if p:
            isWhite = str(p).isupper()
            self.piece_counts[isWhite][p.piece_type] -= 1
        elif mv.promotion is not None:
            isWhite = str(mv.promotion).isupper()
            self.piece_counts[isWhite][mv.promotion] += 1
            self.piece_counts[isWhite][chess.PAWN] -= 1

        self.board.push(mv)


    def generate_successor(self, mv):
        """
        Generate successor board given move mv without modifying the true board.
        """
        new_board = deepcopy(self)
        new_board.move(mv)
        return new_board


    def is_game_over(self):
        """
        Return true if all of one player's pieces have been consumed.
        """

        for k in self.piece_counts:
            if sum(self.piece_counts[k].values()) == 0:
                return True
            # TODO this should go away, but currently not all draws are registering
            # TODO turns out pawn promotions aren't figuring in for piece counts
            else:
                print self.piece_counts[k].values()
        return False


    # TODO not sure this is what we want
    def is_draw(self):
        """
        Return true if there are only kings left.
        """
        if not self.no_kings:
            for color in [chess.WHITE, chess.BLACK]:
                if not sum(self.piece_counts[color].values()) == 1 and self.piece_counts[color][chess.KING] == 1:
                    return False
            print 'we think there are only kings left?'
            return True

        return False

    def piece_at(self, square):
        return self.board.piece_at(square)

    def pieces(self, ptype, color):
        return self.board.pieces(ptype, color)

    def has_kingside_castling_rights(self, color):
        return self.board.has_kingside_castling_rights(color)

    def has_queenside_castling_rights(self, color):
        return self.board.has_queenside_castling_rights(color)

    def has_legal_en_passant(self):
    	return self.board.has_legal_en_passant()

    def ep_square(self):
    	return self.board.ep_square

    def turn(self):
    	return self.board.turn

    def is_seventyfive_moves(self):
        return self.board.is_seventyfive_moves()

    def __str__(self):
        return str(self.board)



