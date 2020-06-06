from PyQt5 import QtCore, QtGui, QtWidgets
import blackboard , class_checker
import os,sys
transform_dict_to_pix = { (x,y):( (x+1)*60 , (y+1)*60 ) for x in range(8) for y in range(8) }
transform_dict_to_08 =  { (x,y):( int((x/60-1)) , int((y/60-1)) ) for x in range(60,481,60) for y in range(60,481,60)}
gridSlotSize = 60
margin = 60
checkerSize = 50
checkerMargin = (gridSlotSize - checkerSize) / 2
gridCount = 8
gridSize = margin + gridSlotSize * gridCount + margin

class CheckerItem(QtWidgets.QGraphicsEllipseItem):
	'''class of visual checker '''
	def __init__(self, player, parent):
		QtWidgets.QGraphicsEllipseItem.__init__(self, parent)
		self.setRect(checkerMargin, checkerMargin, checkerSize, checkerSize)
		if player == 1:
			self.color = QtGui.QColor(QtCore.Qt.darkMagenta)
		else:
			self.color = QtGui.QColor(QtCore.Qt.blue)
		self.activeColor = self.color.lighter()#when we choose the checker
		self.setBrush(self.color)

	def changeColor(self,color):#!!

		'''changing color of checker . Exm: queen '''
		self.color=color #!! why when i do this my color change , but not with setBrush
		self.activeColor=self.color.lighter()

	def setActive(self, active):
		'''changing color when checker is current (player choose checker to move)'''
		if active:
			self.setBrush(self.activeColor)
		else:
			self.setBrush(self.color)

class CheckerScene(QtWidgets.QGraphicsScene):
	#when figure crashes in logic part of game this method activates
	signaldel = QtCore.pyqtSignal(int, int)
	#1-draw ; 2-winner
	EndGameSignal=QtCore.pyqtSignal([],[str])
	#when checher up to queen
	queen_transformation=QtCore.pyqtSignal(int,int)
	#4 buttons on hte scene
	enabling_buttons=QtCore.pyqtSignal(int)
	def __init__(self):
		QtWidgets.QGraphicsScene.__init__(self)
		# scene congifuratios
		self.setSceneRect(margin, margin, gridCount * gridSlotSize, gridCount * gridSlotSize)
		self.addRect(self.sceneRect())

		# create signal . It will be emit() from blackboard.crash()
		self.signaldel.connect(self.del_item)
		#change color of visual checker to show player that it is a queen
		self.queen_transformation.connect(self.queen_transformation_func)
		#choosing the visual checker and its coordinates
		self.current = None

		self._from_=()
		self._to_  =()

		#list of grids and checkers
		self.grid = []
		self.white_checkers = []
		self.black_checkers = []
		for row in range(8):
			for column in range(8):
				# this is a "trick" to make the grid creation easier: it creates
				# a grid square only if the row is odd and the column is even,
				# and viceversa.
				if (not row & 1 and column & 1) or (row & 1 and not column & 1):
					# create a gridItem with a rectangle that uses 0-based
					# coordinates, *then* we set its position
					gridItem = self.addRect(0, 0, gridSlotSize, gridSlotSize)
					gridItem.setPos(margin + column * gridSlotSize, margin + row * gridSlotSize)
					gridItem.setBrush(QtGui.QColor(QtCore.Qt.lightGray))
					self.grid.append(gridItem)
					if 3 <= row <= 4:
						# don't add checkers in the middle
						continue
					# create checkers being careful to assign them the gridItem
					# as a *parent*; their coordinate will *always* be relative
					# to the parent, so that if we change it, they will always
					# be centered
					if row < 3:
						self.black_checkers.append(CheckerItem(0, gridItem))#!
					else:
						self.white_checkers.append(CheckerItem(1, gridItem))#!


		first_palyer_name,second_playr_name,h,m,s = self.get_game_info()
		self.additionsl__init__(first_palyer_name,second_playr_name,h,m,s)



	def get_game_info(self):

		with open('game.txt',"r") as f :
			name1,name2,time=f.read().split(",")
			h,m,s=time.split(":")

			return name1,name2,h,m,s


	def timerEvent(self):
		if self.now_move==0:
			if self.timer2.isActive():
				self.timer2.stop()
			self.timer1.start()
			self.time1 = self.time1.addSecs(-1)
			timestr1 = self.time1.toString("hh:mm:ss")
			self.label1.setText(timestr1)
			if timestr1=="00:00:00":
				self.timer1.stop()
				self.timer2.stop()
				self.EndGameSignal[str].emit(self.player2.name)

		else:
			if self.timer1.isActive():
				self.timer1.stop()
			self.timer2.start()
			self.time2 = self.time2.addSecs(-1)
			timestr2 = self.time2.toString("hh:mm:ss")
			self.label2.setText(timestr2)
			if timestr2=="00:00:00":
				self.timer1.stop()
				self.timer2.stop()
				self.EndGameSignal[str].emit(self.player1.name)

	def get_visual_white_checkers(self):
		return self.white_checkers

	def get_visual_black_checkers(self):
		return self.black_checkers

	def additionsl__init__(self,first_palyer_name,second_player_name,h,m,s):
		'''game_process'''

		self.label2 = QtWidgets.QLabel()
		self.label2.setStyleSheet("QLabel{overflow:hidden;background-color: transparent !important; }")
		self.label2.setGeometry(210, 5, 180, 50)
		self.label2.setFont(QtGui.QFont('SansSerif', 20))
		self.label2.setAlignment(QtCore.Qt.AlignCenter)
		self.label1 = QtWidgets.QLabel()
		self.label1.setStyleSheet("QLabel{overflow:hidden;background-color: transparent !important; }")
		self.label1.setGeometry(210, 545, 180, 50)
		self.label1.setFont(QtGui.QFont('SansSerif', 20))
		self.label1.setAlignment(QtCore.Qt.AlignCenter)
		self.addWidget(self.label2)
		self.addWidget(self.label1)

		# i can connect timer to player
		self.timer1 = QtCore.QTimer()
		self.time1 = QtCore.QTime(int(h), int(m), int(s))
		self.timer1.timeout.connect(self.timerEvent)
		self.timer1.start(1000)

		self.timer2 = QtCore.QTimer()
		self.time2 = QtCore.QTime(int(h), int(m), int(s))
		self.timer2.timeout.connect(self.timerEvent)
		self.timer2.start(1000)
		self.timer2.stop()

		self.label1.setText(self.time1.toString("hh:mm:ss"))
		self.label2.setText(self.time2.toString("hh:mm:ss"))

		self.player1=Player(class_checker.Color.white,first_palyer_name)
		self.player2=Player(class_checker.Color.black,second_player_name)
		self.statusgame=1
		self.now_move=0
		self.moves=0

	def check_status(self):
		'''give us information about game process'''
		if not self.player1.get_figures() :
			self.EndGameSignal[str].emit(self.player2.name)
		if not self.player2.get_figures() :
			self.EndGameSignal[str].emit(self.player1.name)
		pl1_can_move=class_checker.Checker.have_any_moves(self.player1.get_figures())
		pl2_can_move=class_checker.Checker.have_any_moves(self.player2.get_figures())
		if not pl2_can_move and pl1_can_move and self.now_move==1 :
			self.EndGameSignal[str].emit(self.player1.name)
		if not pl1_can_move and pl2_can_move and self.now_move==0:
			self.EndGameSignal[str].emit(self.player2.name)
		'''if not pl1_can_move and not pl2_can_move : # Draw can't be exist !!!!!!
			self.EndGameSignal.emit()'''

	def change_now_move(self):
		'''change the flag-move'''
		self.now_move=1-self.now_move
		#activate buttons / disactivate
		self.enabling_buttons.emit(self.now_move)

	@QtCore.pyqtSlot(int,int)
	def del_item(self,x_del,y_del):
		'''deleting visual checker from the scene'''
		# transform to 08 format
		x_pix,y_pix=transform_dict_to_pix[x_del,y_del]
		items=self.items(QtCore.QPointF(x_pix,y_pix))
		#coord of checker , which will be deleted
		item=items[0].childItems()[0]
		# removing from list of visual checkers
		if item in self.black_checkers :
			self.black_checkers.remove(item)
		else :
			self.white_checkers.remove(item)
		#remove checker from the scene
		self.removeItem(item)

	@QtCore.pyqtSlot(int,int)
	def queen_transformation_func(self,x,y):
		x_pix, y_pix = transform_dict_to_pix[x,y]
		items = self.items(QtCore.QPointF(x_pix, y_pix))
		# coord of checker , which will be deleted
		item = items[0].childItems()[0]

		if item in self.black_checkers :
			item.changeColor(QtGui.QColor(QtCore.Qt.black))
		else :
			item.changeColor(QtGui.QColor(QtCore.Qt.red))

	def mousePressEvent(self, event):
		# right button to deleselect
		if event.button() == QtCore.Qt.RightButton:
			self.setCurrent()
			return
		# find items at the event position, in descending order, top to bottom
		scenePos = event.scenePos()
		items = self.items(scenePos)

		if not items:
			self.setCurrent()
			return

		if isinstance(items[0], QtWidgets.QGraphicsEllipseItem):
			# we found a checker!
			self.setCurrent(items[0] , scenePos) #!

		elif items[0] in self.grid:
			# we found a grid item!
			gridItem = items[0]
			if gridItem.childItems():
				# if it has a checker in it, select it!
				self.setCurrent(gridItem.childItems()[0],scenePos) #!

			elif self.current:
				# no checker here, but if we have a previous one selected
				# we "move" it here, by changing its parent to the new grid item

				self._to_= scenePos.x(), scenePos.y()  # !

				try :
					# do a move in blackboard
					blackboard.table.get_FigureByPosition( *transform_dict_to_08[tuple(map(lambda x : x//60*60,
					self._from_))]).moving(*transform_dict_to_08[tuple(map(lambda x : x//60*60,self._to_))],
										   scene=self) # !
				#KeyError raised sometimes
				except (class_checker.ErrorMove ,KeyError,AttributeError) :# this type exception was imported from class_checker
					self.setCurrent()
				else :
					# if all good - do move on scene
					self.current.setParentItem(gridItem)

					self.setCurrent() #!

					self.change_now_move()  #!
					self.check_status()
					#print (blackboard.table)

	def setCurrent(self, new=None, scenePos=None): #!
		# if a previous checker is selected, deselect it
		if self.current:
			self.current.setActive(False)
			self._from_ = () # !
		self.current = new
		if new is not None  :

			#! if new in now_move player figures - okay else break
			if self.now_move==0:
				if new in self.white_checkers:
					# set the current checker!
					self.current.setActive(True)
					self._from_ = scenePos.x(),scenePos.y() # !
				else:
					pass
			else:
				if new in self.black_checkers:
					# set the current checker!
					self.current.setActive(True)
					self._from_ = scenePos.x(), scenePos.y()  # !

				else :
					pass

class Player():

	def __init__(self,color,name):
		self.name=name
		self.color = color
		self.figures = class_checker.BlackChecker.list_of_checkers if color == class_checker.Color.black \
			else class_checker.WhiteChecker.list_of_checkers
		self.status = None

	def get_status(self):
		return self.status

	def change_status(self, status):
		self.status = status

	def get_figures(self):
		return self.figures

class Checkers(QtWidgets.QWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setObjectName('MainWidget')
		self.setStyleSheet('''#MainWidget {
		                background-color: #267;
		            }''')
		self.setFixedSize(620,800)
		self.start_screen()
		self.Initialization()
		self.checkerScene.EndGameSignal.connect(self.handler_EndGameSignal_draw)
		self.checkerScene.EndGameSignal[str].connect(self.handler_EndGameSignal_win)
		self.checkerScene.enabling_buttons.connect(self.handler_button_enbl)




	def Initialization(self):

		try :
			with open('game.txt',"r") as f :
				name1,name2,time=f.read().split(",")
				h,m,s=time.split(":")
				if len(s)>2 or len(m)>2 or len(h)>2 or len(name1)>11 or len(name2)>11 or ("\n") in f or \
					int(h) > 23 or int(m)>59 or int(s)>59 :
					raise Exception

		except:
			with open('game.txt',"w") as f :
				f.write("Player1,Player2,00:15:00")
				name1="Player1"
				name2="Player2"

		layout = QtWidgets.QGridLayout()
		self.setLayout(layout)

		self.player2Label = QtWidgets.QLabel(name2)
		self.player2Label.setFont(QtGui.QFont('SansSerif', 20))
		layout.addWidget(self.player2Label,0,0)
		self.player2Label.setAlignment(QtCore.Qt.AlignCenter)

		self.button_layout_black=QtWidgets.QHBoxLayout()
		self.button_draw_2=QtWidgets.QPushButton("Button 1 ")#!
		self.button_draw_2.setEnabled(False)
		self.button_giveup_2= QtWidgets.QPushButton("Button 2 ")#!
		self.button_giveup_2.setEnabled(False)
		self.button_draw_2.setMinimumWidth(150)
		self.button_giveup_2.setMinimumWidth(150)
		self.button_draw_2.setText("Предложить ничью !")
		self.button_giveup_2.setText("Сдаюсь !")
		self.button_layout_black.addStretch(1)
		self.button_layout_black.addWidget(self.button_draw_2)
		self.button_layout_black.addWidget(self.button_giveup_2)
		self.button_layout_black.addStretch(1)
		layout.addLayout(self.button_layout_black,1,0)

		self.checkerView = QtWidgets.QGraphicsView()
		layout.addWidget(self.checkerView)
		self.checkerScene = CheckerScene()
		self.checkerView.setScene(self.checkerScene)
		self.checkerView.setFixedSize(gridSize, gridSize)
		# set the Antialiasing render hints to paint "smoother" shapes
		self.checkerView.setRenderHints(QtGui.QPainter.Antialiasing)

		self.button_layout_white = QtWidgets.QHBoxLayout()
		self.button_draw_1 = QtWidgets.QPushButton("Button 3 ")  # !
		self.button_giveup_1 = QtWidgets.QPushButton("Button 4 ")  # !
		self.button_draw_1.setMinimumWidth(150)
		self.button_giveup_1.setMinimumWidth(150)
		self.button_draw_1.setText("Предложить ничью !")
		self.button_giveup_1.setText("Сдаюсь !")
		self.button_layout_white.addStretch(1)
		self.button_layout_white.addWidget(self.button_draw_1)
		self.button_layout_white.addWidget(self.button_giveup_1)
		self.button_layout_white.addStretch(1)
		layout.addLayout(self.button_layout_white, 3, 0)

		self.player1Label = QtWidgets.QLabel(name1)
		self.player1Label.setFont(QtGui.QFont('SansSerif', 20))
		layout.addWidget(self.player1Label,4,0)
		self.player1Label.setAlignment(QtCore.Qt.AlignCenter)

		self.button_giveup_1.clicked.connect(self.handler_button_winsignsimulate)
		self.button_draw_1.clicked.connect(self.handler_button_drawsign)
		self.button_giveup_2.clicked.connect(self.handler_button_winsignsimulate)
		self.button_draw_2.clicked.connect(self.handler_button_drawsign)

	def handler_button_drawsign(self):
		'''if one of the players want DRAW'''
		if self.checkerScene.now_move==0:
			res = QtWidgets.QMessageBox.question(self,f"Ответ игрока {self.checkerScene.player2.name} :",f'Согласен '
																										 f'ли игрок {self.checkerScene.player2.name} на ничью',
											 QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
												 QtWidgets.QMessageBox.No)
		else:
			res = QtWidgets.QMessageBox.question(self, f"Ответ игрока {self.checkerScene.player1.name}",f'Согласен ли игрок {self.checkerScene.player2.name} на ничью',
												 QtWidgets.QMessageBox.Yes |QtWidgets.QMessageBox.No,
												 QtWidgets.QMessageBox.No)
		if res == QtWidgets.QMessageBox.Yes:
			self.checkerScene.EndGameSignal.emit()
		else:
			pass

	def handler_button_winsignsimulate(self):
		'''when palyer want to lose'''
		self.checkerScene.EndGameSignal[str].emit(self.checkerScene.player2.name if self.checkerScene.now_move==0 else
											 self.checkerScene.player1.name)

	@QtCore.pyqtSlot(int)
	def handler_button_enbl(self,now_move):
		'''chaging enabling of buttons'''
		if now_move==0:
			self.button_draw_1.setEnabled(1)
			self.button_giveup_1.setEnabled(1)
			self.button_draw_2.setEnabled(0)
			self.button_giveup_2.setEnabled(0)
		else :
			self.button_draw_1.setEnabled(0)
			self.button_giveup_1.setEnabled(0)
			self.button_draw_2.setEnabled(1)
			self.button_giveup_2.setEnabled(1)

	@QtCore.pyqtSlot(str)
	def handler_EndGameSignal_win(self, result):
		'''show th eresult to players and ask for the next actions (exit,rematch) '''
		res=QtWidgets.QMessageBox.question(self,f"Выиграл {result}","Сиграть еще раз ?",QtWidgets.QMessageBox.Yes |
											 QtWidgets.QMessageBox.No,QtWidgets.QMessageBox.No)

		with open("game.txt","a") as f :
			f.write(f"\n\n#{result} - Winner ")
		if res == QtWidgets.QMessageBox.Yes :
			self.close()
			restart()

		else :
			sys.exit(1)

	@QtCore.pyqtSlot()
	def handler_EndGameSignal_draw(self):
		'''DRAW'''

		res = QtWidgets.QMessageBox.question(self, f"НИЧЬЯ !", "Сиграть еще раз ?",
											   QtWidgets.QMessageBox.Yes |
											   QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
		with open("game.txt", "a") as f :
			f.write(f"\n\n#Draw!! ")
		if res == QtWidgets.QMessageBox.Yes:

			self.close()
			restart()
		else:
			sys.exit(1)


	def start_screen(self):
		'''Loading Screen ONLY FOR BEAUTIFUL START'''
		import time
		splash = QtWidgets.QSplashScreen(QtGui.QPixmap("DIY.jpg"))
		splash.showMessage("Загрузка данных... ",
						   QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.yellow)

		splash.show()
		for i in range(30,101 ,30):
			time.sleep(0.8)
			splash.showMessage(f"Загрузка данных... {i}% ",
							   QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.yellow)


def main():
	import sys
	app = QtWidgets.QApplication(sys.argv)
	checkers = Checkers()
	checkers.show()
	sys.exit(app.exec_())

def restart():

	os.system("python stackoverflow.py")
	sys.exit(0)

if __name__ == '__main__':
	main()