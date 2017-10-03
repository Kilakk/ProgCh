# minesweeper I guess
from tkinter import *
from tkinter import messagebox
import random
from collections import deque

class Tile:

	def __init__(self, frame, mined, coord, nearby):
	
		self.nearby = nearby
		
		# tile is unclicked when first created
		# 0 = unclicked
		# 1 = clicked
		# 2 = flagged
		# 3 = false flag
		# 4 = revealed mine
		self.state = 0
		
		self.mine = mined
		self.coords = coord
		

		self.buttonObject = Button(frame, image = tile_plain)
		self.updateGFX()
		
	def updateGFX(self):
		gfx = tile_plain
	
		if self.getState() > 0:
			if self.getState() == 1:
				if self.numNearby() > 0:
					gfx = tile_no[self.numNearby() - 1]
				elif self.isMine():
					gfx = tile_mine
				else:
					gfx = tile_clicked
				
			elif self.getState() == 2:
				gfx = tile_flag
			elif self.getState() == 3:
				gfx = tile_wrong
			elif self.getState() == 4:
				gfx = tile_mine
			else:
				messagebox.showinfo("Error!", "Error in tile" + str(self.getCoords()) + ": invalid state of " + str(self.getState()) + "!")	
		
		self.buttonObject.config(image = gfx)
		
	def setNearby(self, numnearby):
		self.nearby = numnearby
		
	def setState(self, newstate):
		self.state = newstate
		self.updateGFX()
		
	def setFlagged(self):
		self.setState(2)
		
	def setUnflagged(self):
		self.setState(0)
		
	def setClicked(self):
		self.setState(1)
		
	def getButton(self):
		return self.buttonObject
		
	def isMine(self):
		return self.mine
		
	def isUnclicked(self):
		return self.getState() == 0
		
	def isClicked(self):
		return self.getState() == 1
		
	def isFlagged(self):
		return self.getState() == 2
		
	def getState(self):
		return self.state
		
	def getCoords(self):
		return self.coords
		
	def numNearby(self):
		return self.nearby
		
	def revealMine(self):
		if self.isMine():
			if not self.isFlagged():
				self.setState(4)
		elif self.isFlagged():
			self.setState(3)

class Minesweeper:

	def __init__(self, master):
	
		# define global images
		global tile_plain
		global tile_clicked
		global tile_mine
		global tile_flag
		global tile_wrong
		global tile_no

		# import images
		tile_plain = PhotoImage(file = "images/tile_plain.gif")
		tile_clicked = PhotoImage(file = "images/tile_clicked.gif")
		tile_mine = PhotoImage(file = "images/tile_mine.gif")
		tile_flag = PhotoImage(file = "images/tile_flag.gif")
		tile_wrong = PhotoImage(file = "images/tile_wrong.gif")
		tile_no = []
		for x in range(1, 9):
			tile_no.append(PhotoImage(file = "images/tile_" + str(x) + ".gif"))
		
		# build a frame
		frame = Frame(master)
		frame.pack()
		
		# place title in grid
		self.titleLabel = Label(frame, text = "Minesweeper!")
		self.titleLabel.grid(row = 0, column = 0, columnspan = 10)
		
		# flag variables
		self.flags = 0
		self.correct_flags = 0
		self.clicked = 0
		
		# mine variables
		self.nummines = 0
		
		# create tile objects
		self.tiles = dict({})
		for x in range(0, 10):
			for y in range(0, 10):
				self.tiles[x, y] = Tile(frame, self.randomMine(), (x, y), 0)
				
				# bind clicks to functions
				self.tiles[x, y].getButton().bind('<Button-1>', self.leftClickWrapper((x, y)))
				self.tiles[x, y].getButton().bind('<Button-3>', self.rightClickWrapper((x, y)))
				
		# put tiles on the screen
		for key in self.tiles:
			self.tiles[key].getButton().grid( row = key[0] + 1, column = key[1] )
			
		# find nearby mines and update tile objects
		self.calculateNearby()
			
		# place mine and flag info labels in grid
		self.mineLabel = Label(frame, text = "Mines: " + str(self.numMines()))
		self.mineLabel.grid(row = 11, column = 0, columnspan = 5)
		
		self.flagLabel = Label(frame, text = "Flags: " + str(self.numFlags()))
		self.flagLabel.grid(row = 11, column = 4, columnspan = 5)
	
	def randomMine(self):
		result = random.uniform(0.0, 1.0)
		
		if result < 0.1:
			self.addMine()
			return True
		else: return False
		
	def calculateNearby(self):
		for key in self.tiles:
		
			# it's already a mine, dumbass program
			if self.checkTile(key): continue
		
			nearby = 0
			
			for x in range(key[0] - 1, key[0] + 2):
				for y in range(key[1] - 1, key[1] + 2):
					testkey = (x, y)
					
					if self.checkTile(testkey): nearby += 1
			
			self.tiles[key].setNearby(nearby)
		
	def checkTile(self, key):
		try:
			return self.tiles[key].isMine()
			
		# ignore if we go out of bounds
		except KeyError:
			pass
			
	def checkClicked(self, key):
		try:
			return self.tiles[key].isClicked()
		except KeyError:
			pass
			
	def leftClickWrapper(self, key):
		return lambda Button: self.leftClick(key)
		
	def rightClickWrapper(self, key):
		return lambda Button: self.rightClick(key)
		
	def leftClick(self, key):
		tile = self.tiles[key]
	
		# it's a mine, rip
		if tile.isMine(): 
			self.loseGame()
		elif not self.checkClicked(key):
			tile.setClicked()
			self.clicked += 1
			
			# if it's clear, clear others nearby
			if tile.numNearby() == 0:
				self.clearNearby(key)
			
			if self.isWinner(): self.winGame()
		
	def rightClick(self, key):
		tile = self.tiles[key]
		
		# not clicked
		if tile.isUnclicked():
			tile.setFlagged()
			tile.getButton().unbind('<Button-1>')
			self.addFlag(tile)
		
		# flagged
		elif tile.isFlagged():
			tile.setUnflagged()
			tile.getButton().bind('<Button-1>', self.leftClickWrapper(key))
			self.removeFlag(tile)
			
		self.updateFlagLabel()
		
	def loseGame(self):
		self.revealAllMines()
		messagebox.showinfo("Game Over!", "You ripped really hard... sorry!")
		global root
		root.destroy()
		
	def winGame(self):
		self.revealAllMines()
		messagebox.showinfo("Game Over!", "You win! Congratulations!")
		global root
		root.destroy()
		
	def clearNearby(self, main_key):
		# clear nearby tiles that are blank (where nearby == 0)
		
		# recurse without recursion
		queue = deque([main_key])
		
		while len(queue) > 0:
			key = queue.popleft()
		
			for x in range(key[0] - 1, key[0] + 2):
				for y in range(key[1] - 1, key[1] + 2):
					testkey = (x, y)
					# print("Clearing nearby: testing key " + str(testkey))
				
					# don't reclick ourselves. ignore ones we already clicked.
					if not testkey == key and not self.checkClicked(testkey):
						# check if it's clear
						if self.checkClear(testkey):
							self.tiles[testkey].setClicked()
							queue.append(testkey)
							self.clicked += 1
							
						# clear the first numbered tile, if it's not a mine
						elif not self.checkTile(testkey):
							try:
								self.tiles[testkey].setClicked()
								self.clicked += 1
							except KeyError:
								pass
		
	def checkClear(self, key):
		try:
			return self.tiles[key].numNearby() == 0
		except KeyError:
			pass
		
	def updateFlagLabel(self):
		self.flagLabel.config(text = "Flags: " + str(self.numFlags()))
		
	def isWinner(self):
		if self.clicked == 100 - self.nummines: return True
		else: return False
		
	def addMine(self):
		self.nummines += 1
		
	def numMines(self):
		return self.nummines
		
	def numFlags(self):
		return self.flags
		
	def addFlag(self, tile):
		self.flags += 1
		
		if tile.isMine():
			self.correct_flags += 1
		
	def removeFlag(self, tile):
		self.flags -= 1
		
		if tile.isMine():
			self.correct_flags -= 1
			
	def revealAllMines(self):
		for key in self.tiles:
			self.tiles[key].revealMine()

def main():
	sys.setrecursionlimit(15000)

	global root
	root = Tk()
	root.title("Minesweeper!")
	
	minesweeper = Minesweeper(root)
	
	root.mainloop()
	
	
if __name__ == "__main__":
	main()