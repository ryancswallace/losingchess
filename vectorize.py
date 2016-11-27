import chess
import losing_board

# this case handles promotions easily
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
    
    # castling rights
    out_vec.append(1) if board.has_kingside_castling_rights(chess.WHITE) else out_vec.append(0)
    out_vec.append(1) if board.has_kingside_castling_rights(chess.BLACK) else out_vec.append(0)
    out_vec.append(1) if board.has_queenside_castling_rights(chess.WHITE) else out_vec.append(0)
    out_vec.append(1) if board.has_queenside_castling_rights(chess.BLACK) else out_vec.append(0)

    # en passant rights
    if board.has_legal_en_passant():
        out_vec.append(board.ep_square())
    else:
        out_vec.append(0)

    # turn
    out_vec.append(int(board.turn()))
    
    return out_vec

# promotions much more difficult here
# instead of full encoding of promotions, we follow Lai and use piece counts
def piece_vector(board):
    out_vec = []
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    white_counts = [0] * 6
    black_counts = [0] * 6

    for ptype in piece_types:
        white_set = board.pieces(ptype, chess.WHITE)
        black_set = board.pieces(ptype, chess.BLACK)
        
        # encode existence and type of promotions by piece counts but not locations
        white_counts[ptype - 1] = len(white_set)
        black_counts[ptype - 1] = len(black_set)

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
            for q_square in white_set:
                out_vec.append(q_square + 1)
            out_vec += [0] * (1- len(white_set))
            for q_square in black_set:
                out_vec.append(q_square + 1)
            out_vec += [0] * (1 - len(black_set))
        else:
            for k_square in white_set:
                out_vec.append(k_square + 1)
            out_vec += [0] * (1 - len(white_set))
            for k_square in black_set:
                out_vec.append(k_square + 1)
            out_vec += [0] * (1 - len(black_set))

    # promotions via piece counts
    out_vec += white_counts
    out_vec += black_counts

    # castling rights
    out_vec.append(1) if board.has_kingside_castling_rights(chess.WHITE) else out_vec.append(0)
    out_vec.append(1) if board.has_kingside_castling_rights(chess.BLACK) else out_vec.append(0)
    out_vec.append(1) if board.has_queenside_castling_rights(chess.WHITE) else out_vec.append(0)
    out_vec.append(1) if board.has_queenside_castling_rights(chess.BLACK) else out_vec.append(0)

    # en passant rights
    if board.has_legal_en_passant():
        out_vec.append(board.ep_square())
    else:
        out_vec.append(0)

    # turn
    out_vec.append(int(board.turn()))

    return out_vec


# b = losing_board.LosingBoard(no_kings=False)
# print piece_vector(b)
# moves = b.get_legal_moves()
# b.move(moves[0])
# print piece_vector(b)
# moves = b.get_legal_moves()
# b.move(moves[0])
# print piece_vector(b)

