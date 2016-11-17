import numpy as np
from copy import deepcopy

class losingChess:

	def __init__(self, size=8):

		if size <= 6:
			raise Exception("Game must be of size at least 7 (by 7)")

		self.size = size

		self.board = np.array([['R','N','B','Q','K','B','N','R'],
							  ['P']*size,
							  ['']*size, ['']*size,['']*size,['']*size,
							  ['p']*size,
							  ['r','n','b','q','k','b','n','r']])
		self.turn = 'W'
		self.consumedPieces = {'W': [], 'B': []}

		# hard code dynamics of the game ... is this best?
		self.dynamics = {'p': [[1,0]], 
						   'n': [[3,1], [3,-1], [-3,1], [-3,-1]],
						   'b': [[y,x] for x, y in zip(range(size), range(size))] 
						   		+ [[-y,x] for x, y in zip(range(size), range(size))]
						   		+ [[y,-x] for x, y in zip(range(size), range(size))] 
						   		+ [[-y,-x] for x, y in zip(range(size), range(size))],
						   'q': [None],
						   'k': [[y,x] for y in range(-1,2) for x in range(-1,2)],
						   'r': [[y,0] for y in range(-size+1, size)] + [[0,x] for x in range(-size+1, size)]}
		
		for k, v in self.dynamics.items():
			v = [np.array(tup) for tup in v]
			self.dynamics[k] = v


	def getMoves(self, piecePos):
		"""
			Input:  [int, int]       piecePos 		
			Output: [[int, int],...] legalMoves
		"""
		piece = self.board[piecePos[0], piecePos[1]]
		isBlack = piece.islower()
		direction = 1 - 2*isBlack
		pieceType = piece.lower()

		possMoves = self.dynamics[pieceType]

		# helper to check if a position is on the board
		onBoard = lambda pos: pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8

		legalDestinations = []

		for move in possMoves:
			newPos = piecePos + move*direction
			# check if new position would be on the board
			if onBoard(newPos):
				# check if there is no piece or a capturable piece at the possible destination
				if self.board[newPos[0], newPos[1]] == '' or self.board[newPos[0], newPos[1]].islower() != isBlack:
					legalDestinations.append(newPos)

		# pawn exception
		if pieceType == 'p':
			posPawnMoves = [piecePos + [1,1]*direction, piecePos + [1,-1]*direction]
			for newPos in posPawnMoves:
				if self.board[newPos[0], newPos[1]] != '' and self.board[newPos[0], newPos[1]].islower() != isBlack:
					legalDestinations.append()

		return legalDestinations

	def evaluateMove(self, cur, nxt, evalFun):
		"""
			Evaluate possible board position board given next move
		"""
		posBoard = deepcopy(self.board)

		posNextBoard = self.move(cur, nxt, posBoard)

		return evalFun(posNextBoard)


	def move(self, cur, nxt, altBoard=None):
		"""
			Move piece at position cur to next if legal.
			Given an altBoard (alternative board for state evaluation purposes),
			execute the move on a copy of the current board and return it.
			Otherwise, execute the move on the game board.
		"""

		# check if move is legal
		if tuple(nxt) not in [tuple(mv) for mv in self.getMoves(cur)]:
			raise Exception("Enter a legal move!")

		brd = None
		if altBoard:
			brd = altBoard
		else:
			brd = self.board

		# remove opponent's piece if necessary
		dest = self.board[nxt[0], nxt[1]]
		if dest != '':
			if dest.islower():
				self.consumedPieces['W'].append(dest)
			else:
				self.consumedPieces['B'].append(dest)

		# move piece
		self.board[nxt[0], nxt[1]] = self.board[cur[0], cur[1]]
		self.board[cur[0], cur[1]] = ""


		if altBoard:
			return brd
		else:
			self.board = brd
			return None

"""
--> Agent Class that takes in gameState
--> Additional exceptions (castling, promotions, etc.)
"""




