import random
import os
from Config import *

class Tile():
	def __init__(self) -> None:
		self.Options = list(TileRules.keys())
		self.Entropy = len(self.Options)
		self.Neighbours = dict()

	def AddNeighbour(self, dir, tile):
		self.Neighbours[dir] = tile

	def UpdateEntropy(self):
		self.Entropy = len(self.Options)
	
	def Collapse(self):
		self.Options = [self.Options[random.randint(0, self.Entropy-1)]]
		self.UpdateEntropy()

	# dirFrom - Direction, relative to the tile, of the semi-collapsed tile
	# options - Possible tiles that the semi-collapsed tile can take
	def Restrict(self, dirFrom, options):
		changed = False

		if self.Entropy != 1:
			connections = []
			for option in options:
				connections.append(TileRules[option][dirFrom])

			dirFacing = None
			if dirFrom == NORTH: dirFacing = SOUTH
			if dirFrom == EAST:  dirFacing = WEST
			if dirFrom == SOUTH: dirFacing = NORTH
			if dirFrom == WEST:  dirFacing = EAST

			for option in self.Options.copy():
				if TileRules[option][dirFacing] not in connections:
					self.Options.remove(option)
					changed = True

			self.UpdateEntropy()

		return changed

class WFCGenerator():
	def __init__(self, rows, cols):
		self.Rows = rows
		self.Cols = cols
		self.Grid = []
		self.Images = []

		for x in range(rows):
			for y in range(cols):
				tile = Tile() # Need to use lvalue to create instance 
				self.Grid.append(tile)

		for x in range(rows):
			for y in range(cols):
				tile = self.Grid[x + y * cols]

				if y > 0:
					tile.AddNeighbour(NORTH, self.Grid[x + (y-1) * cols])
				if x < rows - 1:
					tile.AddNeighbour(EAST, self.Grid[(x+1) + y * cols])
				if y < cols - 1:
					tile.AddNeighbour(SOUTH, self.Grid[x + (y+1) * cols])
				if x > 0:
					tile.AddNeighbour(WEST, self.Grid[(x-1) + y * cols])

	def GetLowestEntropy(self):
		lowestEntropy = len(list(TileRules.keys()))
		tiles = []

		for x in range(self.Rows):
			for y in range(self.Cols):
				tile = self.Grid[x + y * self.Cols]
				if tile.Entropy != 1:
					if tile.Entropy == lowestEntropy:
						tiles.append(tile)
					if tile.Entropy < lowestEntropy:
						tiles = [tile]
						lowestEntropy = tile.Entropy

		return tiles

	def Collapse(self):
		# Collapse random tile to begin
		low = self.GetLowestEntropy()

		if low == []:
			return

		startTile = low[random.randint(0, len(low)-1)]
		startTile.Collapse()

		uncollapsedTiles = [startTile]

		while uncollapsedTiles != []:
			tile = uncollapsedTiles.pop()
			for dir in list(tile.Neighbours.keys()):
				neighbourTile = tile.Neighbours[dir]
				changed = neighbourTile.Restrict(dir, tile.Options)
				if changed:
					uncollapsedTiles.append(neighbourTile)
		
		# print("===========")
		# for y in range(self.Rows):
		# 	for x in range(self.Cols):
		# 		print(f"{x}, {y}: {self.Grid[x + y * self.Cols].Options}")

		self.Collapse()
	
	def LoadImages(self, load):
		for imagePath in TileImagePaths:
			img = load(os.path.join('assets', imagePath))
			self.Images.append(img)