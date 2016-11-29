import vectorize

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
		        mv, val = agent.get_move(self.board, return_value=True)
		        position_values.append(val)
		        if not mv:
		            outer_break = True
		            print "It's a draw."
		            break
		        self.board.move(mv)


		        print "Agent " + str(turn + 1) + " makes move: "+ str(mv)
		        print self.board
		        print
		        print vectorize.piece_vector(self.board)
		        print 

		        turn = not turn

		        if self.board.is_game_over():
		            print
		            print "Agent " + str(turn + 1) + " victorious in " + str(self.board.board.fullmove_number) + " plies."
		            print
		            outer_break = True
		            break
		        if self.board.is_draw():
		            print "It's a draw in " + str(self.board.board.fullmove_number) + " plies."
		            print
		            draw = True
		            break

		    if outer_break: break

		    turn_num += 1
		    if max_turns != None:
				if 2 * turn_num >= max_turns: break

		return position_values

