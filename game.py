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
        turn_num = 0
        while True:
            outer_break = False
            turn = False
            for agent in [self.a1,self.a2]:
                res = agent.get_move(self.board, return_value=True)
                if res is None:
                    outer_break = True
                    print "Because it's a stalemate, Agent " + str(turn + 1) + " victorious!"
                    break
                else:
                    mv, val = res
                    position_values.append(val)
                    if self.board.is_seventyfive_moves():
                        outer_break = True
                        print "It's a draw due to 75 moves."
                        break
                    if not mv:
                        # TODO this case might not be necessary
                        outer_break = True
                        print "Because it's a stalemate, Agent " + str(turn + 1) + " victorious!"
                        break
                self.board.move(mv)


                print "Agent " + str(turn + 1) + " makes move: "+ str(mv)
                print self.board
                print

                turn = not turn

                if self.board.is_game_over():
                    print
                    print "Agent " + str(turn + 1) + " victorious in " + str(self.board.board.fullmove_number) + " plies."
                    print
                    outer_break = True
                    break

            if outer_break: break

            turn_num += 1
            if max_turns != None:
                if 2 * turn_num >= max_turns: break

        return position_values

# example run with softmax
sm_model = softmax.Softmax(1000, 3000, 0.01)
sm_model.train(print_accuracy=False)

sm_eval = evaluation.SoftmaxEval(sm_model)
eval1 = sm_eval.softmax_eval
eval2 = sm_eval.softmax_eval

a1 = chess_agents.AlphaBetaAgent(color=chess.WHITE, eval_func=eval1, depth='0')
a2 = chess_agents.AlphaBetaAgent(color=chess.BLACK, eval_func=eval2, depth='0')
board = losing_board.LosingBoard(no_kings=False)

game = Game(board, a1, a2)
game.play()
