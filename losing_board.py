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
            # take out castling moves
            out_moves = [move for move in list(chess_legal_moves) if not self.board.is_castling(move)]
            return out_moves

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

        # make move
        self.board.push(mv)

        # update piece counts
        for color in [chess.WHITE, chess.BLACK]:
            for piece_type in [chess.PAWN, chess.ROOK, chess.BISHOP, chess.QUEEN, chess.KING, chess.KNIGHT]:
                pieces = self.board.pieces(piece_type, color)
                if pieces is not None:
                    self.piece_counts[color][piece_type] = len(pieces)
                else:
                    self.piece_counts[color][piece_type] = 0

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
            if all(v == 0 for v in self.piece_counts[k].values()):
                return True
        return False

    def winner_by_pieces(self):
        """
        Return chess.WHITE if white has fewer peices, chess.BLACK if black has fewer, 0.5 if same
        """
        num_white = 0
        num_black = 0
        for piece_type in [chess.PAWN, chess.ROOK, chess.BISHOP, chess.QUEEN, chess.KING, chess.KNIGHT]:
            num_white += len(self.board.pieces(piece_type, chess.WHITE))
            num_black += len(self.board.pieces(piece_type, chess.BLACK))

        if num_white < num_black:
            return chess.WHITE
        elif num_white > num_black:
            return chess.BLACK
        elif num_white == num_black:
            return 0.5
        else:
            raise Exception('Impossible.')

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

    def is_attacked_by(self, color, square):
        return self.board.is_attacked_by(color, square)

    def __str__(self):
        builder = []

        # get most recent move
        last_move = str(self.board.peek())
        last_move_start = last_move[:2]
        last_move_end = last_move[2:]

        # handle square moved from
        start_rank = ord(last_move_start[0]) - ord('a')
        start_file = int(last_move_start[1])
        start_green_square = (start_file - 1) * 8 + start_rank

        # handle square moved to
        end_rank = ord(last_move_end[0]) - ord('a')
        end_file = int(last_move_end[1])
        end_green_square = (end_file - 1) * 8 + end_rank

        for square in chess.SQUARES_180:
            piece = self.piece_at(square)

            if piece:
                sym = piece.symbol()
                if square == end_green_square:
                    # green
                    builder.append("\033[32m" + sym + "\033[0m")
                elif sym.isupper():
                    # red
                    builder.append("\033[31m" + sym + "\033[0m")
                else:
                    # blue
                    builder.append("\033[34m" + sym + "\033[0m")
            else:
                if square == start_green_square:
                    # green background
                    builder.append("\033[42m \033[0m")
                else:
                    builder.append(".")

            if chess.BB_SQUARES[square] & chess.BB_FILE_H:
                if square != chess.H1:
                    builder.append("\n")
            else:
                builder.append(" ")

        return "".join(builder)
        # return str(self.board)

