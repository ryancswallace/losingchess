import chess
import losing_board

l = losing_board.LosingBoard()
l.move(chess.Move.from_uci('g2g4'))
l.move(chess.Move.from_uci('f7f5'))
print l.getLegalMoves()