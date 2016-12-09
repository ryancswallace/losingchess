import vectorize

"""
Here we will build the processes that drive games between two AIs,
and games between an AI and a human.
Perhaps we'll use command line arguments to select agent types,
evaluation functions, number of AIs, a la Berkeley.
"""


class Game:
    def __init__(self, board, a1, a2, get_stats=False):
        self.board = board or LosingBoard()
        self.a1 = a1
        self.a2 = a2
        self.get_stats = get_stats

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
                move_val_pair = agent.get_move(self)

                # if there are no moves to be made
                if move_val_pair is None:
                    outer_break = True
                    winner = self.board.winner_by_pieces()
                    if winner == 0.5:
                        # print "It's a draw in " + str(self.board.board.fullmove_number) + " plies.\n"
                        # print str(self.board.board.fullmove_number)
                        if self.get_stats:
                            return None
                    else:
                        agent_num = 2 if int(winner) == 0 else 1
                        # print "Because it's a stalemate, Agent " + str(agent_num) + " victorious in " \
                        #       + str(self.board.board.fullmove_number) + " plies!"
                        # print str(self.board.board.fullmove_number)

                        if self.get_stats:
                            return winner
                
                # if there are moves to be made
                else:
                    # make move and if agent 1 keep track of board and values
                    if type(move_val_pair) == tuple:
                        mv, val = move_val_pair
                    else:
                        mv, val = move_val_pair, None
                    self.board.move(mv)
                    if agent == self.a1:
                        position_values.append(val)
                        board_vectors.append(vectorize.piece_vector(self.board))

                    # print "Agent " + str(turn + 1) + " makes move: "+ str(mv)
                    # print self.board
                    # print '\n'

                    # switch players
                    turn = not turn

                    if self.board.is_seventyfive_moves():
                        outer_break = True
                        # print "It's a draw due to 75 moves."
                        # print str(self.board.board.fullmove_number)

                        if self.get_stats:
                            return None

                    if self.board.is_game_over():
                        # print "Agent " + str(turn + 1) + " victorious in " + str(self.board.board.fullmove_number) + " plies.\n"
                        # print str(self.board.board.fullmove_number)
                        
                        if self.get_stats:
                            return turn == 0
                        outer_break = True

            # update turn numbers
            if max_turns != None and self.board.board.fullmove_number >= max_turns: 
                outer_break = True

            # check that game didn't end on last move
            if outer_break:
                break

        return position_values, board_vectors
