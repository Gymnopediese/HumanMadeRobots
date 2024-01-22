import sys

import random

class TicTacToe:
    
	PLAYERAMMOUNT = 2

	def __init__(self, players) -> None:
		self.players = random.shuffle(players)
		self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
		self.player = 1

	def state(self):
		return self.board

	def move(self, move):
		try:
			if self.board[int(move[0])][int(move[1])] != 0:
				return False
			self.board[int(move[0])][int(move[1])] = self.player
		except:
			return False
		self.player += 1
		if (self.player > self.PLAYERAMMOUNT):
			self.player = 1
		return True

	def check_win(self):
		for i in range(3):
			if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
				return self.board[i][0]
			if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
				return self.board[0][i]
		if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
			return self.board[0][0]
		if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
			return self.board[0][2]
		return 0

	def check_draw(self):
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == 0:
					return False
		return True
		
	def possible_moves(self):
		moves = []
		for i in range(3):
			for j in range(3):
				if self.board[i][j] == 0:
					moves.append([i, j])
		return moves

	def best_move(self):
		bot = self.player
		moves = self.possible_moves()
		if len(moves) == 9:
			return [0, 0]
		best_move = moves[0]
		minmax = -2
		for	move in moves:
			self.board[move[0]][move[1]] = bot
			move_value = self.rec((bot % 2) + 1, bot, 0)
			if minmax < move_value:
				best_move = move
				minmax = move_value
			self.board[move[0]][move[1]] = 0
		return best_move

	def rec(self, current_player, bot, depth):
		winner = self.check_win()
		if winner == bot:
			return 9 - depth
		elif winner != 0:
			return -9 + depth
		elif self.check_draw():
			return 0
		if current_player == bot:
			minmax = -10
		else:
			minmax = 10
		moves = self.possible_moves()
		for	move in moves:
			self.board[move[0]][move[1]] = current_player
			if (current_player == bot):
				minmax = max(minmax, self.rec((current_player) % 2 + 1, bot,  depth + 1))
			else:
				minmax = min(minmax, self.rec((current_player) % 2 + 1, bot,  depth + 1))
			self.board[move[0]][move[1]] = 0
		return minmax
