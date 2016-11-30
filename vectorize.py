import chess
import losing_board

# this case handles promotions easily
# TODO does it need turn information encoded?
def square_vector(board):
    out_vec = []
    all_squares = chess.SquareSet(chess.BB_ALL)
    for square in all_squares:
        piece = board.piece_at(square)
        if piece is None:
            out_vec.append(0)
        elif piece.symbol() == 'P':
            out_vec.append(1)
        elif piece.symbol() == 'p':
            out_vec.append(2)
        elif piece.symbol() == 'N':
            out_vec.append(3)
        elif piece.symbol() == 'n':
            out_vec.append(4)
        elif piece.symbol() == 'B':
            out_vec.append(5)
        elif piece.symbol() == 'b':
            out_vec.append(6)
        elif piece.symbol() == 'R':
            out_vec.append(7)
        elif piece.symbol() == 'r':
            out_vec.append(8)
        elif piece.symbol() == 'Q':
            out_vec.append(9)
        elif piece.symbol() == 'q':
            out_vec.append(10)
        elif piece.symbol() == 'K':
            out_vec.append(11)
        elif piece.symbol() == 'k':
            out_vec.append(12)
    out_vec.append(1) if board.has_kingside_castling_rights(chess.WHITE) else out_vec.append(0)
    out_vec.append(1) if board.has_kingside_castling_rights(chess.BLACK) else out_vec.append(0)
    out_vec.append(1) if board.has_queenside_castling_rights(chess.WHITE) else out_vec.append(0)
    out_vec.append(1) if board.has_queenside_castling_rights(chess.BLACK) else out_vec.append(0)

    # still need to add en passant rights - will need to look at movestack and put in the move

    return out_vec

# promotions much more difficult here
def piece_vector(board):
    out_vec = []
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    for ptype in piece_types:
        white_set = board.pieces(ptype, chess.WHITE)
        black_set = board.pieces(ptype, chess.BLACK)
        if ptype == chess.PAWN:
            for p_square in white_set:
                out_vec.append(p_square + 1)
            out_vec += [0] * (8 - len(white_set))
            for p_square in black_set:
                out_vec.append(p_square + 1)
            out_vec += [0] * (8 - len(black_set))
        elif ptype == chess.KNIGHT:
            for n_square in white_set:
                out_vec.append(n_square + 1)
            out_vec += [0] * (2 - len(white_set))
            for n_square in black_set:
                out_vec.append(n_square + 1)
            out_vec += [0] * (2 - len(black_set))
        elif ptype == chess.BISHOP:
            for b_square in white_set:
                out_vec.append(b_square + 1)
            out_vec += [0] * (2 - len(white_set))
            for b_square in black_set:
                out_vec.append(b_square + 1)
            out_vec += [0] * (2 - len(black_set))
        elif ptype == chess.ROOK:
            for r_square in white_set:
                out_vec.append(r_square + 1)
            out_vec += [0] * (2 - len(white_set))
            for r_square in black_set:
                out_vec.append(r_square + 1)
            out_vec += [0] * (2 - len(black_set))
        elif ptype == chess.QUEEN:
            # TODO do players have to take queen promotions? Could there be 9 total?
            for q_square in white_set:
                out_vec.append(q_square + 1)
            out_vec += [0] * (9 - len(white_set))
            for q_square in black_set:
                out_vec.append(q_square + 1)
            out_vec += [0] * (9 - len(black_set))
        else:
            for k_square in white_set:
                out_vec.append(k_square + 1)
            out_vec += [0] * (1 - len(white_set))
            for k_square in black_set:
                out_vec.append(k_square + 1)
            out_vec += [0] * (1 - len(black_set))

        # probably still need the same castling and en passant checks from above
        out_vec.append(1) if board.has_kingside_castling_rights(chess.WHITE) else out_vec.append(0)
        out_vec.append(1) if board.has_kingside_castling_rights(chess.BLACK) else out_vec.append(0)
        out_vec.append(1) if board.has_queenside_castling_rights(chess.WHITE) else out_vec.append(0)
        out_vec.append(1) if board.has_queenside_castling_rights(chess.BLACK) else out_vec.append(0)


b = losing_board.LosingBoard(no_kings=True)
print square_vector(b)
