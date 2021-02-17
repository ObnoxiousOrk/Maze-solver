"""
Name: mazeSolver.py
Date Start: 17/2/2021
Date End: 

0 = Walkable
1 = Wall
2 = Start
3 = End
8 = Path
"""

"""
find corners and other nodes, connect, jump node to node to solve
"""

import copy
import numpy as np
from PIL import Image

class MAZE():
	def __init__(self):
		self.maze = []

	def getMaze(self, source="Maze.png"): #--If no maze source is specified, the default is set to Maze.png
		img = Image.open(source).convert("LA") #--Opens the maze image from the file path specified
		aMaze = np.array(img) #--Converts the maze image into an array of colour values for each pixel

		aBoolMaze = []


		#--For each pixel in row in the array of colour values if the pixel is not white, it is a wall and is set to 1, and if it's white, it can be moved on and is set to 0
		for row in aMaze:
			aRow = [] #--At the beginning of every row of pixels, set the array containing information about that row to be blank
			for pixel in row:
				if pixel[0] == 0:
					aRow.append(1)
				else:
					aRow.append(0)

			aBoolMaze.append(aRow) #--Adds the completed row to the whole maze


		return aBoolMaze

	def findStartEnd(self, maze):
		for i in range(len(maze[0])):
			if maze[0][i] == 0: #--If the pixel that is being interrogated on the top line is walkable, it has to be the start, so set it to the start character
				# maze[0][i] = 2
				vStart = [0, i]

				maze[vStart[0]][vStart[1]] = NODE([vStart[0], vStart[1]], False, False, True, False)

		for i in range(len(maze[len(maze)-1])):
			if maze[len(maze)-1][i] == 0: #--If the pixel that is being interrogated on the last line is walkable, it has to be the end, so set it to the end character
				# maze[len(maze)-1][i] = 3
				vEnd = [len(maze)-1, i]

				maze[vEnd[0]][vEnd[1]] = NODE([vEnd[0], vEnd[1]], True, False, False, False)

		return maze

	def mprint(self, maze): #--Displays maze array
		for row in maze:
			print(row)
		print()

	def makeSimpleNodes(self, maze):

		def isNode(coord, count=False, maze=maze): #--Find out if any space is a node by checking if it has more than 2 spaces next to it. WONT FIND ALL NODES!!!
			noEmpty = 0
			
			cNorth = False
			cSouth = False
			cEast = False
			cWest = False

			try:
				if maze[coord[0]+1][coord[1]] == 0 or type(maze[coord[0]+1][coord[1]]) == NODE: #  the space = maze[coord[0]][coord[1]]
					noEmpty += 1
					cSouth = True
				if maze[coord[0]-1][coord[1]] == 0 or type(maze[coord[0]-1][coord[1]]) == NODE:
					noEmpty += 1
					cNorth = True
				if maze[coord[0]][coord[1]+1] == 0 or type(maze[coord[0]][coord[1]+1]) == NODE:
					noEmpty += 1
					cEast = True
				if maze[coord[0]][coord[1]-1] == 0 or type(maze[coord[0]][coord[1]-1]) == NODE:
					noEmpty += 1
					cWest = True
			except IndexError:
				return False

			if count == True:
				if noEmpty > 2:
					return True
				else:
					return False
			else:
				return (cNorth, cEast, cSouth, cWest)


		# return isNode([1, 2])

		aNodes = []

		for row in range(len(maze)):
			for col in range(len(maze[0])):
				if maze[row][col] == 0: #--If any space is empty, check if its a node, if it is, make a node at those coords.
					if isNode([row, col], count=True):
						aNodes.append([row, col])
						cNorth, cEast, cSouth, cWest = isNode([row, col])
						maze[row][col] = NODE([row, col], cNorth, cEast, cSouth, cWest)

		return maze, aNodes

	def findNodeConnections(self, aSimpleNodes): #--Might also find empty nodes? call multiple times?
		nodesLeft = True
		while nodesLeft:
			for row in range(len(self.maze)): #--refresh the list of nodes before every node connection attempt
				for col in range(len(self.maze[0])):
					if type(self.maze[row][col]) == NODE:
						aSimpleNodes.append([row, col])

			for nodePos in aSimpleNodes:
				# print(nodePos)
				self.maze = self.maze[nodePos[0]][nodePos[1]].findNodeConnections(self.maze)
		

	def main(self):
		self.maze = self.getMaze("../Mazes/ManipulatingBadCode.png")

		self.maze = self.findStartEnd(self.maze)
		
		self.maze, aSimpleNodes = self.makeSimpleNodes(self.maze)
		# print(aSimpleNodes)

		self.findNodeConnections(aSimpleNodes)


class NODE():
	def __init__(self, pos, cNorth, cEast, cSouth, cWest):
		self.aPos = pos
		self.connections = { #--Initially set to bool value indicating presence of a connection that way, later look and find where connection is.
		"north" : cNorth,
		"east" : cEast,
		"south" :cSouth,
		"west" : cWest
		}

	def findNodeConnections(self, maze):

		def nodeConnectDir(coord, maze=maze): #--Find out directions a node has connections.
			cNorth = False
			cSouth = False
			cEast = False
			cWest = False

			try:
				if maze[coord[0]+1][coord[1]] == 0 or type(maze[coord[0]+1][coord[1]]) == NODE: #  the space = maze[coord[0]][coord[1]]
					cSouth = True
				if maze[coord[0]-1][coord[1]] == 0 or type(maze[coord[0]-1][coord[1]]) == NODE:
					cNorth = True
				if maze[coord[0]][coord[1]+1] == 0 or type(maze[coord[0]][coord[1]+1]) == NODE:
					cEast = True
				if maze[coord[0]][coord[1]-1] == 0 or type(maze[coord[0]][coord[1]-1]) == NODE:
					cWest = True
			except IndexError:
				return False
			
			return (cNorth, cEast, cSouth, cWest)

		if self.connections["north"] == True:
			currentPos = copy.deepcopy([self.aPos[0]-1, self.aPos[1]])
			foundNode = False
			while foundNode == False:
					if maze[currentPos[0]][currentPos[1]] == 0: #--If not at a node or wall, go one more space
						currentPos[0] -= 1

					elif type(maze[currentPos[0]][currentPos[1]]) == NODE: #--If at a node, set the apt connection to the coord
						self.connections["north"] = currentPos

						foundNode = True

					elif maze[currentPos[0]][currentPos[1]] == 1: #--If at a wall, set the space before to a node
						currentPos[0] += 1
						cNorth, cEast, cSouth, cWest = nodeConnectDir([currentPos[0], currentPos[1]])
						maze[currentPos[0]][currentPos[1]] = NODE([currentPos[0], currentPos[1]], cNorth, cEast, cSouth, cWest)

						foundNode = True

		if self.connections["south"] == True:
			currentPos = copy.deepcopy([self.aPos[0]+1, self.aPos[1]])
			foundNode = False
			while foundNode == False:
					if maze[currentPos[0]][currentPos[1]] == 0: #--If not at a node or wall, go one more space
						currentPos[0] += 1

					elif type(maze[currentPos[0]][currentPos[1]]) == NODE: #--If at a node, set the apt connection to the coord
						self.connections["south"] = currentPos

						foundNode = True

					elif maze[currentPos[0]][currentPos[1]] == 1: #--If at a wall, set the space before to a node
						currentPos[0] -= 1
						cNorth, cEast, cSouth, cWest = nodeConnectDir([currentPos[0], currentPos[1]])
						maze[currentPos[0]][currentPos[1]] = NODE([currentPos[0], currentPos[1]], cNorth, cEast, cSouth, cWest)

						foundNode = True

		if self.connections["east"] == True:
			currentPos = copy.deepcopy([self.aPos[0], self.aPos[1]+1])
			foundNode = False
			while foundNode == False:
					if maze[currentPos[0]][currentPos[1]] == 0: #--If not at a node or wall, go one more space
						currentPos[1] += 1

					elif type(maze[currentPos[0]][currentPos[1]]) == NODE: #--If at a node, set the apt connection to the coord
						self.connections["east"] = currentPos

						foundNode = True

					elif maze[currentPos[0]][currentPos[1]] == 1: #--If at a wall, set the space before to a node
						currentPos[1] -= 1
						cNorth, cEast, cSouth, cWest = nodeConnectDir([currentPos[0], currentPos[1]])
						maze[currentPos[0]][currentPos[1]] = NODE([currentPos[0], currentPos[1]], cNorth, cEast, cSouth, cWest)

						foundNode = True

		if self.connections["west"] == True:
			currentPos = copy.deepcopy([self.aPos[0], self.aPos[1]-1])
			foundNode = False
			while foundNode == False:
					if maze[currentPos[0]][currentPos[1]] == 0: #--If not at a node or wall, go one more space
						currentPos[1] -= 1

					elif type(maze[currentPos[0]][currentPos[1]]) == NODE: #--If at a node, set the apt connection to the coord
						self.connections["west"] = currentPos

						foundNode = True

					elif maze[currentPos[0]][currentPos[1]] == 1: #--If at a wall, set the space before to a node
						currentPos[1] += 1
						cNorth, cEast, cSouth, cWest = nodeConnectDir([currentPos[0], currentPos[1]])
						maze[currentPos[0]][currentPos[1]] = NODE([currentPos[0], currentPos[1]], cNorth, cEast, cSouth, cWest)

						foundNode = True






solve = MAZE()
# maze = [[1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 1, 1]]
newMaze = solve.main()
solve.mprint(solve.maze)
# solve.mprint(newMaze)
# print(solve.maze[1][6].connections["west"])