import random
from functools import reduce
from game.Game import Game
from copy import deepcopy
import sys
class HighLow(Game):
    

	GAME_NAME = "HighLow"
	SYMBOLES = ["+", "-", "*", "/","sqt"]
	CHANGEABLE = ["+", "-", "*"]
	PHASE_VALIDATING_HANDS = 0
	PHASE_BETTING = 1
	PHASE_REVEALING = 2
	DECK =[str(i) + ["g", "s", "c", "b"][j] for i in range(11) for j in range(4)]
	DECK += ["sqt", "sqt", "sqt", "sqt", "*", "*", "*", "*"]
 
	def __init__(self, players, playground=False) -> None:
		super().__init__()
		random.shuffle(players)
		self.players = players
		self.playground = playground
		if playground:
			self.players = ["a", "b", "c", "d"]
		self.history = []
		self.me = 0
		self.draw_cards()
  
	def draw_cards(self):
		self.minbest = [9999, 43]
		self.maxbest = [-9999, 0]

		self.minwinner = 0
		self.maxwinner = 0

		self.minormax = []
		self.result = []
		self.in_game_players = deepcopy(self.players)
		self.private = []
		self.hands = [[] for _ in range(len(self.players))]
		self.deck = deepcopy(self.DECK)
		random.shuffle(self.deck)
		for _ in range(len(self.players)):
			card = self.deck.pop()
			while card == "*" or card == "sqt":
				card = self.deck.pop()
			self.private.append(card)
		for hand in self.hands:
			for _ in range(3):
				card = self.deck.pop()
				hand.append(card)
				if card == "*" or card == "sqt":
					while card == "*" or card == "sqt":
						card = self.deck.pop()
					hand.append(card)
			hand += ["+", "-", "/"]
		for i, j in zip(self.private, self.hands):
			print(i, j)

		self.phase = self.PHASE_VALIDATING_HANDS
		self.player = self.valid_hands()

	def valid_move(self, move):
		index = self.player - 1
		for card in move:
			if not card in self.hands[index] or card != self.private[index]:
				raise Exception({"stderr": "invalid move: " + str(move)})
		if len(move) != len(self.hands[index]) + 1:
			raise Exception({"stderr": "invalid move: " + str(move)})
		return self.evaluate_move(move)
  
	def evaluate_move(self, move):
		def rec(move):
			if len(move) == 0 or (len(move) == 1 and move[0] in self.SYMBOLES):
				return False
			if len(move) == 1:
				print(move)
				return int(move[0][:-1])
			for symb in self.SYMBOLES:
				for card in move:
					if symb == card:
						right = rec(move[move.index(card) + 1:])
						if right == False:
							return False
						if symb == "sqt":
							return right ** (1 / 2)
						left = rec(move[:move.index(card)])
						if left == False:
							return False
						if symb == "+":
							return left + right
						if symb == "-":	
							return left - right
						if symb == "*":
							return left * right
						if symb == "/":	
							return left / right
			raise Exception({"stderr": "invalid move: " + str(move)})
		res = rec(move)
		move = [i for i in move if not i in self.SYMBOLES]
		move.sort(key=lambda x: ["b", "c", "s", "g"].index(x[-1]))
		move.sort(key=lambda x: int(x[:-1]))
		return res, move[0], move[-1]
				
	def state(self):
		return {"hands": [hand + [self.private[self.player - 1]] if self.player == i else hand for i, hand in enumerate(self.hands)], "me": self.me, "phase": self.phase}

	def valid_hands(self):
		for i, hand in enumerate(self.hands):
			if len([i for i in hand if i in self.CHANGEABLE]) > 2:
				return i + 1
		self.phase = self.PHASE_BETTING
		return 1

	def move(self, move):
		if self.phase == self.PHASE_VALIDATING_HANDS:
			if not move in self.CHANGEABLE or not move in self.hands[self.player - 1]:
				raise Exception({"stderr": "invalid move: " + str(move)})
			self.hands[self.player - 1].remove(move)
			self.player = self.valid_hands()
		elif self.phase == self.PHASE_BETTING:
			self.player += 1
			if self.move != 0 or self.move != 1:
				raise Exception({"stderr": "invalid move: " + str(move)})
			self.minormax.append(move)
		elif self.phase == self.PHASE_REVEALING:
			move, mini, maxi = self.valid_move(move)
			if self.minormax[self.player] == 0:
				if (move == self.minbest[0] and self.DECK.index(mini) < self.minbest[1])\
    			or abs(1 - move) < abs(1 - self.minbest[0]):
					self.minbest = [move, self.DECK.index(mini)]
					self.minwinner = self.player
			else:
				if (move == self.maxbest[0] and self.DECK.index(maxi) > self.maxbest[1])\
        		or abs(20 - move) < abs(20 - self.minbest[0]):
					self.maxbest = [move, self.DECK.index(maxi)]
					self.maxwinner = self.player
			self.player += 1
	def check_win(self):
		return False

	def check_draw(self):
		return False
# game = HighLow(["a", "b", "c", "d"])

# print(game.evaluate_move(["1g", "+", "2g"]))
# print(game.evaluate_move(["1g", "+", "1b", "*", "sqt", "9g", "/", "9s"]))

# print(game.state())