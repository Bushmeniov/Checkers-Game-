# Module : class_checker
import blackboard

to_abc_format={1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h'}

class ErrorMove(Exception):
	def __init__(self,message):
		self.message=message

class Color():
	white=0
	black=1

class Checker():
	# PARENT CLASS

	IMG=("🅦",'🅑')

	'''list of 4 around positions'''

	possible_positions = (("x+1", "y-1"),
						  ("x-1", "y-1"),
						  ("x-1", "y+1"),
						  ("x+1", "y+1"),)

	'''We check if two checkers are in one line . After pos x+1,y-1 ... is pos x+2,y-1 ... '''
	ppp = (("x+2", "y-2"),
		   ("x-2", "y-2"),
		   ("x-2", "y+2"),
		   ("x+2", "y+2"),)

	def __init__(self,coordinate,color):
		self.color=color
		self.IMG='🅑' if color==Color.black else "🅦" # !
		self.coordinate=coordinate

	def __repr__(self):
		return self.IMG

	def get_chechers(self):
		return self.list_of_checkers

	def get_position(self):
		return self.coordinate

	def change_coordinate(self,x,y):
		self.coordinate=(x,y)

	def get_possible_positions(self):
		return Checker.possible_positions

	def get_ppp(self):
		return Checker.ppp

	def FindEnemyNearFigure(self,enemy_color):

		'''
			if one has an opponent near  :
				if NOT after this opponent is other object :
					add to list_of_move possible coord to move , and coord of del enemy to list_of_pop
			:return: list_of_move,list_of_pop if list_of_pop	else False
		'''

		list_of_move=[] #to crash
		list_of_pop=[] #del enemy

		get_figure = blackboard.table.get_FigureByPosition  # link on the table method

		possible_positions=self.get_possible_positions()
		ppp=self.get_ppp()

		x, y = self.get_position()  # figure position

		for pp in range(len(possible_positions)):
			'''   x_   after figure (pps_pos) coordinates;
				  x__  2after figure (ppp)    coordinates '''
			x_ = eval(possible_positions[pp][0])
			y_ = eval(possible_positions[pp][1])
			if x_ < 0 or y_ < 0 or x_ > 7 or y_ > 7:
				continue
			figure_after = get_figure(x_, y_)  # get object, which is in the next position (emty or figure)
			if figure_after and figure_after.color == enemy_color:
				x__ = eval(ppp[pp][0])
				y__ = eval(ppp[pp][1])
				if x__ < 0 or y__ < 0 or x__ > 7 or y__ > 7:
					continue
				if not get_figure(x__, y__):
					list_of_move.append( (x__,y__) )
					list_of_pop.append( (x_,y_) )

		return (list_of_move,list_of_pop) if list_of_pop else False

	@classmethod
	def FindEnemyNear(cls, enemy_color):
		'''
		Go throw all black checkers and check ..
			if the figure has an enemy near  (func FundEnemyNearFigure )
				 append this figure to a dict of HAVE_TO_CRASH
		:return: HAVE_TO_CRASH if HAVE_TO_CRASH else 0
		'''

		HAVE_TO_CRASH={}

		for figure in cls.list_of_checkers:
			res=figure.FindEnemyNearFigure(enemy_color)

			if res != False :
				list_of_move,list_of_pop=res
				'''move - possible moves to crash opponent's checker
				   pop - opponet's checker, which will be deleted, after move '''
				HAVE_TO_CRASH[figure] = {'move': list_of_move, "pop": list_of_pop}
			else :
				continue

		return HAVE_TO_CRASH if HAVE_TO_CRASH else False

	@staticmethod
	def have_any_moves(figures): # this method for draw
		'''
		We go throw a pattern moves (posssible_pos) and check it witch a .move(self,x_to,y_to). func  .
		We can add a flag check or really move to that func .

		find enemy near can check and move can check !!

		:param figures: figures of player
		:return: True or False
		'''

		for figure in figures :

			if figure.FindEnemyNearFigure(1-figure.color):
				return True

			if figure.can_figure_move() :
				return True
		return False

	def can_figure_move(self): # from have_any_moves_func
		'''we check if figure can move
		to do this , we use method move in this class '''
		x,y=self.get_position()
		for coord in self.get_possible_positions():
			if self.move(eval(coord[0]), eval(coord[1]),1):
				return True
		return False

	def makeamove(self,x_to,y_to,scene=None):

		'''Move figure from one place to another'''

		x, y = self.get_position()  # pos of object now

		f = open("game.txt", 'a')
		if scene.now_move == 0 :
			scene.moves+=1
			f.write(f"\n{scene.moves}. {to_abc_format[x+1]}{8-y} {to_abc_format[x_to+1]}{8-y_to} -")
			f.close()
		else :
			f.write(f" {to_abc_format[x+1]}{8-y} {to_abc_format[x_to+1]}{8-y_to}")
			f.close()

		'''if y_to != 7 and y_to != 0 : # if not transfrom to
				#  Quuen
			blackboard.table.swap_iconvalues(self,x,y,x_to,y_to)'''

		if y_to == 7 and self.color==Color.black:
			BlackChecker.list_of_checkers.remove(self) # delete self from list of checkers
			blackboard.table.change_iconvalue(0,x,y) # change value of icon on the board
			blackboard.table.change_iconvalue(BlackQueen((x_to, y_to)) ,x_to,y_to) # change to Quuen
			BlackChecker.list_of_checkers.append(blackboard.table.get_FigureByPosition(x_to,y_to))#add Queen to list
			scene.queen_transformation.emit(x, y) #change visual color of queen
		elif y_to == 0 and self.color==Color.white:
			WhiteChecker.list_of_checkers.remove(self)
			blackboard.table.change_iconvalue(0,x,y)
			blackboard.table.change_iconvalue(WhiteQueen((x_to, y_to)) ,x_to,y_to)
			WhiteChecker.list_of_checkers.append(blackboard.table.get_FigureByPosition(x_to, y_to))# add Queen to list
			scene.queen_transformation.emit(x, y)#change visual color of queen
		else :
			blackboard.table.swap_iconvalues(self,x,y,x_to,y_to)

	def move(self,x_to,y_to,move_or_check=0,scene=None): # move==0 , check = 1 !!!!!!!!!!!!!
		if not 0 <= x_to < 8 or not 0 <= y_to < 8:
			if move_or_check:
				return False
			else:
				raise ErrorMove(" x,y must be in interval 0..7 ")
		x, y = self.get_position()  # pos of object now
		if self.color == Color.black:
			possible_moves = self.get_possible_positions()[2:]
		else:  # self.color == Color.white
			possible_moves = self.get_possible_positions()[:2]

		'''if coordinates on func arg are in possible_moves -> move'''

		try:
			move_successful = False
			if (eval(possible_moves[0][0]) == x_to and eval(possible_moves[0][1]) == y_to and not
			blackboard.table.get_FigureByPosition(x_to, y_to)) or \
					(eval(possible_moves[1][0]) == x_to and eval(possible_moves[1][1]) == y_to and
					 not blackboard.table.get_FigureByPosition(x_to, y_to)):
				move_successful = True
			if not move_successful:
				if move_or_check:
					return False
				else:
					raise ErrorMove("Coordinate x_to,y_to not in possible moves")
		except ValueError:
			print("Try to choose coordinates again ")
		else:
			if move_or_check:
				return True
			else:
				self.makeamove(x_to,y_to,scene=scene)

	def crash(self,x_to,y_to,HAVE_TO_CRASH,scene ) :
		x, y = self.get_position()  # pos of object now
		try:
			move_successful = False  # flag
			for coord in range(len(HAVE_TO_CRASH[self]['move'])): # go throw possible crash values
				if x_to == HAVE_TO_CRASH[self]['move'][coord][0] and y_to == HAVE_TO_CRASH[self]['move'][coord][1]:
					x_del, y_del = HAVE_TO_CRASH[self]['pop'][coord] # coord of del figure
					move_successful = True
			if not move_successful:
				raise ErrorMove ("You must crash enemy,but your x_to,y_to not in possible crash values of the figure.")  #	!!!
		except ValueError:
			print("Try to choose coordinates again ")
		else:
			obj_del=blackboard.table.get_FigureByPosition(x_del,y_del) # obj which will del
			if obj_del.__class__==BlackChecker or obj_del.__class__==BlackQueen: # check the list which will use to del
				BlackChecker.list_of_checkers.remove(obj_del)#del obj
				#self.VISUAL_del_item(x_del,y_del) # VISUAL
				scene.signaldel.emit(x_del, y_del)

			else:
				WhiteChecker.list_of_checkers.remove(obj_del)

				scene.signaldel.emit(x_del, y_del)

				#self.VISUAL_del_item(x_del, y_del ) # VISUAL

			del obj_del#!
			blackboard.table.change_iconvalue(0,x_del,y_del) # change value of icon of the board
			self.makeamove(x_to, y_to,scene=scene)
			# if after our crash , our figure can crash enemy again
			# i use getfigurebypos func as if my move x_to and y_to may be 0 or 7 ,in this situatin, my object will be
			# changed into queen figure , and SELF will not be exist after this operation
			if blackboard.table.get_FigureByPosition(x_to,y_to).FindEnemyNearFigure(1 - self.color):
				scene.change_now_move()
			else:
				pass

	def moving(self, x_to, y_to,scene ): #
		'''Method which start move process'''
		if not  0<=x_to<8  or  not 0<=y_to<8:

			raise ErrorMove('x,y must be in interval 0..7')

		HAVE_TO_CRASH = self.__class__.FindEnemyNear(1 - self.color)

		if not HAVE_TO_CRASH : # if HAVA_TO_CRASH is empty
			self.move(x_to,y_to ,scene=scene)
		else:
			if self in HAVE_TO_CRASH:
				self.crash(x_to,y_to,HAVE_TO_CRASH,scene)
			else:
				raise ErrorMove('You must crash. Choose the figure,which can crash enemy. ')

class BlackChecker(Checker):

	list_of_checkers=[]

	def __init__(self,coordinate):
		super().__init__(coordinate,Color.black)

class WhiteChecker(Checker):
	list_of_checkers = []

	def __init__(self,coordinate):
		super().__init__(coordinate,Color.white)

class Queen(Checker):
	# not to forget .. after update to Queen change checker object into
	# Queen object in list_of_checkers

	possible_positions = (
		[('x+1', 'y-1'), ('x+2', 'y-2'), ('x+3', 'y-3'), ('x+4', 'y-4'), ('x+5', 'y-5'), ('x+6', 'y-6'),
		 ('x+7', 'y-7')],
		[('x-1', 'y-1'), ('x-2', 'y-2'), ('x-3', 'y-3'), ('x-4', 'y-4'), ('x-5', 'y-5'), ('x-6', 'y-6'),
		 ('x-7', 'y-7')],
		[('x-1', 'y+1'), ('x-2', 'y+2'), ('x-3', 'y+3'), ('x-4', 'y+4'), ('x-5', 'y+5'), ('x-6', 'y+6'),
		 ('x-7', 'y+7')],
		[('x+1', 'y+1'), ('x+2', 'y+2'), ('x+3', 'y+3'), ('x+4', 'y+4'), ('x+5', 'y+5'), ('x+6', 'y+6'),
		 ('x+7', 'y+7')],)

	IMG = ('♕','♛')

	def __init__(self,coordinate,color):
		super().__init__(coordinate)
		self.IMG = '♛' if color == Color.black else '♕'

	def get_possible_positions(self):
		return Queen.possible_positions

	def can_figure_move(self):  # from have_any_moves_func
		'''this is redefined method of Checker class '''
		x,y= self.get_position()
		for line in self.get_possible_positions() :
			for coord in line :
				if self.move(eval(coord[0]),eval(coord[1]),1):
					return True
		return False

	def FindEnemyNearFigure(self, enemy_color):
		'''
		We check all possible_enemy coordinates (Right-UP..)
			if on the road we see an enemy figure :
				we remember this coordinate
				continue to check other coord-s on the line to
				find all empty objects (it will be our possible moves)
				if coord is empty :
					add to move and pop list coordinates
				if  we find the object or the board will end :
					break
		return list of moves and pop figures
		'''

		list_of_move =[]
		list_of_pop  = []

		'''possible_possisions consists of 4 lists . Every list consists of tuples with coordinates. 
		 1 list has RIGHT_UP possible enemy coordinate ; 2 LEFT_UP ; 3 LEFT_DOWN ; 4 RIGHT_DOWN	'''

		get_figure = blackboard.table.get_FigureByPosition  # link on the table method
		x, y = self.get_position()  # figure position

		possible_positions=self.get_possible_positions()

		for line in possible_positions:#!
			for pp in range(len(line)):
				x_=eval(line[pp][0])
				y_=eval(line[pp][1])
				if x_ < 0 or y_ < 0 or x_ > 7 or y_ > 7:
					continue
				figure_after = get_figure(x_, y_)  # get object, which is in the next position (emty or figure)
				if figure_after and figure_after.color == enemy_color and pp+1<7 : # 3 condition  for not IndexError
					for empty_pos in range( pp+1,len(line) ):

						x__=eval(line[empty_pos][0])
						y__=eval(line[empty_pos][1])
						if x__ < 0 or y__ < 0 or x__ > 7 or y__ > 7:
							continue
						if not get_figure(x__, y__):
							list_of_move.append( (x__,y__) )
							list_of_pop.append( (x_,y_) )
						else:
							break

		return (list_of_move,list_of_pop) if list_of_pop else False

	def makeamove(self,x_to,y_to,scene=None):
		'''Move figure from one place to another'''

		x, y = self.get_position()  # pos of object now
		blackboard.table.swap_iconvalues(self,x,y,x_to,y_to)

	def move(self,x_to,y_to,move_or_check=0,scene=None): # move_or_check from func have_any_moves
		'''
		Firstly, we check in what line we must compare our finish coordinate to possible coordinates(RIGHT_UP...)
		succesful_move=False
		for coord in line :
			x,y= self.pos
			eval coordinates == x_to and y_to
			s_m = True
		:param x_to: end coordinate
		:param y_to: end coorditate
		:return:
		'''
		if not 0<=x_to<8  or not 0<=y_to<8:
			if move_or_check :
				return False
			else :
				raise ErrorMove("x,y must be in interval 0..7")

		get_figure = blackboard.table.get_FigureByPosition  # link on the table method

		if x_to-self.coordinate[0] > 0  and y_to-self.coordinate[1] < 0 : # if RIGHT_UP
			possible_positions=self.get_possible_positions()[0]
		elif x_to - self.coordinate[0] < 0 and y_to - self.coordinate[1] < 0: # if LEFT_UP
			possible_positions = self.get_possible_positions()[1]
		elif x_to-self.coordinate[0] < 0  and y_to-self.coordinate[1] > 0 : # if LEFT_DOWN
			possible_positions = self.get_possible_positions()[2]
		else : 																# if RIGHT_DOWN
			possible_positions = self.get_possible_positions()[3]

		succesful_move = False
		x,y=self.get_position()
		for coord in possible_positions:
			# if figure will be before end coord - s_m False
			if eval(coord[0])==x_to and eval(coord[1]) == y_to :
				if not get_figure(x_to,y_to) :
					succesful_move=True
					if move_or_check : # !!!!!!!!!!!!!!!
						return True
					self.makeamove(x_to,y_to)

					break
				else:
					if move_or_check:
						return False #!!!!
					raise ErrorMove("You have a figure in your x_to,y_to coordinates.")
			else :
				if  get_figure(eval(coord[0]),eval(coord[1])): #! i have change params x_to,y_to
					if move_or_check :
						return False # !!!!!!!!
					raise ErrorMove("You have a figure in your way to x_to,y_to coordinates.")
				else:
					continue

class BlackQueen(Queen,BlackChecker):
	def __init__(self,coordinate):
		super().__init__(coordinate,Color.black)

class WhiteQueen(Queen,WhiteChecker):
	def __init__(self,coordinate):
		super().__init__(coordinate,Color.white)


