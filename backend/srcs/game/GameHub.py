
from game.TicTacToe import TicTacToe
from game.Maze import Maze
from game.HighLow import HighLow

def new_game(game_name, players = [], playground = True):
	if game_name == "TicTacToe":
		return TicTacToe(players, playground)
	if game_name == "Maze":
		return Maze(playground)
	if game_name == "HighLow":
		return HighLow(players, playground)
	raise Exception({"stderr": "invalid game name"})
