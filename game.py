import chess

import losing_board
import chess_agents
import softmax
import evaluation

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
        moves_made = []
        while True:
            outer_break = False
            turn = False
            for agent in [self.a1,self.a2]:

                if outer_break:
                    break

                res = agent.get_move(self.board, return_value=True)
                if res is None:
                    outer_break = True
                    print "Because it's a stalemate, Agent " + str(turn + 1) + " victorious!"
                    break
                
                # if there are moves to be made
                else:
                    # keep track of moves and values
                    mv, val = res
                    position_values.append(val)
                    if self.board.is_seventyfive_moves():
                        outer_break = True
                        print "It's a draw due to 75 moves."
                    self.board.move(mv)

                    # print board 
                    print "Agent " + str(turn + 1) + " makes move: "+ str(mv)
                    print self.board
                    print '\n'

                    # switch players
                    turn = not turn

                    if self.board.is_game_over():
                        print
                        print "Agent " + str(turn + 1) + " victorious in " + str(self.board.board.fullmove_number) + " plies."
                        print
                        outer_break = True

            # update turn numbers
            if max_turns != None and self.board.board.fullmove_number >= max_turns: 
                outer_break = True

            # check that game didn't end on last move
            if outer_break: 
                break

        return position_values, moves_made

# example run with softmax
sm_model = softmax.Softmax(3000, 1000, 0.01)
sm_model.train(print_accuracy=True)

sm_eval = evaluation.SoftmaxEval(sm_model)
eval1 = sm_eval.softmax_eval
eval2 = sm_eval.softmax_eval
#
# weighted_counter = evaluation.WeightedPieceCount()
#
a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=eval1, depth='1')
a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=eval2, depth='1')
# a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=weighted_counter.weighted_piece_count, depth='1')
# a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=weighted_counter.weighted_piece_count, depth='1')
board = losing_board.LosingBoard(no_kings=False)

game = Game(board, a1, a2)
game.play()
