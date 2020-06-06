# Module : board
import class_checker

class Board():
	def __init__(self):
		# create an empty deck
		self.deck = [[0 for i in range(8)] for i in range(8)]
		self.createStartPosition()

	def createStartPosition(self):

		first_pos = 1  # corner position
		for raw in range(3):
			for st in range(first_pos, 8, 2):
				b = class_checker.BlackChecker((st, raw))
				self.change_iconvalue(b,st,raw)
				class_checker.BlackChecker.list_of_checkers.append(b)

				w = class_checker.WhiteChecker((7-st, 7-raw))
				self.change_iconvalue(w,7 - st,7-raw )
				class_checker.WhiteChecker.list_of_checkers.append(w)

			first_pos = 1 - first_pos

	def get_deck(self):
		return self.deck

	def change_iconvalue(self,obj,x,y):
		'''change value of icon on the boart. Ex : e4 - checker'''
		self.deck[y][x]=obj # icon value = obj
		if obj!=0:
			obj.change_coordinate(x,y) # change attribute of object

	def swap_iconvalues(self,obj,x,y,x_to,y_to):
		'''swipe icon values'''
		self.deck[y][x], self.deck[y_to][x_to] = self.deck[y_to][x_to], self.deck[y][x]
		obj.change_coordinate(x_to,y_to) # change attribute of object

	def get_FigureByPosition(self,x,y):
		'''get a figure by coordinate'''
		return self.deck[y][x]

	def __repr__(self):
		# deck repl
		res_deck = ""
		for i in range(8):
			res_deck += " ".join(map(str, self.deck[i])) + "\n"
		return res_deck


table=Board()
