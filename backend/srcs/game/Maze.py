
from game.Game import Game
import random
from copy import deepcopy
class Maze(Game):
	
	PLAYERAMMOUNT = 1
	
	def __init__(self, playground = False) -> None:
		super().__init__()
		self.GAME_NAME = "Maze"
		self.player = 1
		self.playground = playground
		self.history = []
		self.pos = [1, 1]
		self.step = 0
		self.new_maze()

  
	def valid_moves(self, move):
		moves = [
			[move[0] - 2, move[1]],
			[move[0], move[1] + 2],
			[move[0] + 2, move[1]],
			[move[0], move[1] - 2]
		]
  
		moves2 = [
			[move[0] - 1, move[1]],
			[move[0], move[1] + 1],
			[move[0] + 1, move[1]],
			[move[0], move[1] - 1]
		]
		valid_moves = []
		for move, move2 in zip(moves, moves2):
			if move[0] >= 0 and move[0] < 10 and move[1] >= 0 and move[1] < 10 and self.board[move2[0]][move2[1]] == 1 and self.board[move[0]][move[1]] == 1:
				valid_moves.append([move2, move])
		return valid_moves
		
	def print(self):
		for i in self.board:
			print(i)
		print()
  
	def new_maze(self):
		self.board = [[1 for i in range(11)] for j in range(11)]
		self.goal = [1, 1]
		snake = [[1, 1]]
		_max = 0
		while True:
			if len(snake) == 0:
				break
			self.board[snake[-1][0]][snake[-1][1]] = 0
			# if random.randint(0, 5) == 0 and len(snake):
			# 	snake.pop()
			# 	continue
			moves = self.valid_moves(snake[-1])
			if len(moves) == 0:
				snake.pop()
				continue
			x = random.choice(moves)
			self.board[x[0][0]][x[0][1]] = 0
			snake.append(x[1])
			if _max < len(snake):
				_max = len(snake)
				self.goal = x[1]
		self.board[self.goal[0]][self.goal[1]] = 2
  
  
	def state(self):
		return {"board": self.board, "position": self.pos}

	# up, right, down, left
	def move(self, move):
		self.step += 1
		moves = [
			[self.pos[0], self.pos[1] - 1],
			[self.pos[0] + 1, self.pos[1] ],
			[self.pos[0], self.pos[1] + 1],
			[self.pos[0] - 1,  self.pos[1] ]
		]
		try:
			if self.board[moves[move][0]][moves[move][1]] == 1:
				raise Exception({"stderr": "invalid move: " + str(move)})
		except Exception as e:
			raise Exception({"stderr": "invalid move: " + str(move)})
		if self.playground:
			self.history.append(deepcopy(self.pos))
		self.pos = moves[move]

	def check_win(self):
		if self.pos == self.goal:
			return 1
		return 0

	def check_draw(self):
		return self.step >= 50

	def possible_moves(self):
		moves = [
			[self.pos[0], self.pos[1] - 1],
			[self.pos[0] + 1, self.pos[1] ],
			[self.pos[0], self.pos[1] + 1],
			[self.pos[0] - 1,  self.pos[1] ]
		]
		valid_moves = []
		for i, move in enumerate(moves):
			if move[0] >= 0 and move[0] < 10 and move[1] >= 0 and move[1] < 10 and self.board[move[0]][move[1]] == 0:
				valid_moves.append(i)
		return valid_moves

	def best_move(self):
		return random.choice(self.possible_moves())
		# initial_pos = self.pos
  
		# moves = self.possible_moves()
		# if len(moves) == 1:
		# 	return moves[0]

		# paths = []
		
		# for move in moves:
		# 	old_pos = self.pos
		# 	self.pos = move
		# 	paths.ap
		# 	self.pos = old_pos

		# self.pos = initial_pos
		
		# return move == 0

	def undo(self):
		if self.playground and len(self.history) > 0:
			self.pos = self.history.pop()