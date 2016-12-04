import chess

import losing_board
import chess_agents
import softmax
import evaluation
import vectorize
import multilayer

"""
Here we will build the processes that drive games between two AIs,
and games between an AI and a human.

Perhaps we'll use command line arguments to select agent types,
evaluation functions, number of AIs, a la Berkeley.
"""
class Game:
    def __init__(self, board, a1, a2):
        self.board = board
        self.a1 = a1
        self.a2 = a2

    def play(self, max_turns=None):
        position_values = []
        board_vectors = []
        while True:
            outer_break = False
            turn = False
            for agent in [self.a1,self.a2]:
                # check that game didn't end on last half-move
                if outer_break:
                    break

                # agent finds best move
                move_val_pair = agent.get_move(self, return_value=True)

                # if there are no moves to be made
                if move_val_pair is None:
                    outer_break = True
                    winner = self.board.winner_by_pieces()
                    if winner == 0.5:
                        print "It's a draw in " + str(self.board.board.fullmove_number) + " plies.\n"
                    else:
                        print "Because it's a stalemate, Agent " + str(int(winner)) + " victorious!"
                
                # if there are moves to be made
                else:
                    # make move and if agent 1 keep track of board and values
                    mv, val = move_val_pair
                    self.board.move(mv)
                    if agent == self.a1:
                        position_values.append(val)
                        board_vectors.append(vectorize.piece_vector(self.board))

                    # print board 
                    print "Agent " + str(turn + 1) + " makes move: "+ str(mv)
                    print self.board
                    print '\n'

                    # switch players
                    turn = not turn

                    if self.board.is_seventyfive_moves():
                        outer_break = True
                        print "It's a draw due to 75 moves."

                    if self.board.is_game_over():
                        print "Agent " + str(turn + 1) + " victorious in " + str(self.board.board.fullmove_number) + " plies.\n"
                        outer_break = True

            # update turn numbers
            if max_turns != None and self.board.board.fullmove_number >= max_turns: 
                outer_break = True

            # check that game didn't end on last move
            if outer_break: 
                break

        return position_values, board_vectors


# multilayer_model = multilayer.Mutlilayer(10, 10, 1, 1, vectorize.piece_count_vector, vectorize.piece_count_vector_len())
# multilayer_model.train()

# multilayer_model = evaluation.MultilayerEval(multilayer_model)
# eval1 = multilayer_model.multilayer_eval
# eval2 = multilayer_model.multilayer_eval

sm_model = softmax.Softmax(10, 10, 1, 1, vectorize.piece_vector, vectorize.piece_vector_len())
sm_model.train(print_accuracy=True)

sm_eval = evaluation.SoftmaxEval(sm_model)
eval1 = sm_eval.softmax_eval
eval2 = sm_eval.softmax_eval
#
weighted_counter = evaluation.WeightedPieceCount()
# #
a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=eval1, depth='1')
a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=eval2, depth='1')
# a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=weighted_counter.weighted_piece_count, depth='1')
# a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=weighted_counter.weighted_piece_count, depth='1')
board = losing_board.LosingBoard(no_kings=False)

game = Game(board, a1, a2)
game.play()
