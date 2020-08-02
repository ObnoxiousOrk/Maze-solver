import copy
import numpy as np
from PIL import Image

class NODE():
	def __init__(self, aPos):
		self.aPos = aPos

		self.aUp = []
		self.aLeft = []
		self.aRight = []
		self.aDown = []

	def assignConnection(self, vDir, aCoords):
		if vDir == "Up":
			self.aUp = aCoords
		elif vDir == "Left":
			self.aLeft = aCoords
		elif vDir == "Right":
			self.aRight = aCoords
		elif vDir == "Down":
			self.aDown = aCoords
		else:
			print("Invlid Maze")


class MAZE():
	def __init__(self, maze):
		self.aMazeUnsolved = self.getMaze(maze) #--Initilises the instance variable in the array with the value returned from the getMaze function

		self.aMazeNodes = self.createNodes()

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

	def displayMaze(self, maze):
		#--Prints each row 1 after the other
		for row in maze:
			aRow = []
			for space in row:
				if isinstance(space, NODE):
					aRow.append(8)
				else:
					aRow.append(space)
			print(aRow)

	def findStartEnd(self):
		for i in range(len(self.aMazeUnsolved[0])):
			if self.aMazeUnsolved[0][i] == 0: #--If the pixel that is being interrogated on the top line is walkable, it has to be the start, so set it to the start character
				aStart = [0, i]

		for i in range(len(self.aMazeUnsolved[len(self.aMazeUnsolved)-1])):
			if self.aMazeUnsolved[len(self.aMazeUnsolved)-1][i] == 0: #--If the pixel that is being interrogated on the last line is walkable, it has to be the end, so set it to the end character
				aEnd = [len(self.aMazeUnsolved)-1, i]

		return aStart, aEnd

	def createNodes(self):

		def countNodes(aSegment):
			vCount = 0

			for i in aSegment:
				if isinstance(i, NODE):
					vCount += 1
				else:
					pass

			return vCount

		# def makeConnectionDownLeft(aSegmentDown, aSegmentLeft):
		# 	if countNodes(aSegmentDown) >= 2:
		# 		aNodeIndeciesDown = []
		# 		for i in range(len(aSegmentDown)):
		# 			if isinstance(aSegmentDown[i], NODE):
		# 				aNodeIndeciesDown.append(i)

		# 		print(aNodeIndeciesDown)

		# 		if all(pos == 0 for pos in aSegmentDown[aNodeIndeciesDown[0] + 1:aNodeIndeciesDown[1]]):
		# 			aMazeNodes[aSegmentDown[aNodeIndeciesDown[0]].aPos[0]][aSegmentDown[aNodeIndeciesDown[0]].aPos[1]].assignConnection("Down", aSegmentDown[aNodeIndeciesDown[1]].aPos)
		# 			aMazeNodes[aSegmentDown[aNodeIndeciesDown[1]].aPos[0]][aSegmentDown[aNodeIndeciesDown[1]].aPos[1]].assignConnection("Up", aSegmentDown[aNodeIndeciesDown[0]].aPos)
					
		# 			del aSegmentDown[aNodeIndeciesDown[0]:aNodeIndeciesDown[1]]

		# 			aNodeIndeciesDown.pop(0)
		# 			print(aNodeIndeciesDown, aSegmentDown)

		# 	if countNodes(aSegmentLeft) >= 2:
		# 		aNodeIndeciesLeft = []
		# 		for i in range(len(aSegmentLeft)):
		# 			if isinstance(aSegmentLeft[i], NODE):
		# 				aNodeIndeciesLeft.append(i)

		# 		print("Indicies:", aNodeIndeciesLeft)


		# 		print(aSegmentLeft[aNodeIndeciesLeft[0] + 1:aNodeIndeciesLeft[1]])
		# 		if all(pos == 0 for pos in aSegmentLeft[aNodeIndeciesLeft[0] + 1:aNodeIndeciesLeft[1]]):
		# 			print(aMazeNodes[aSegmentLeft[aNodeIndeciesLeft[0]].aPos[0]][aSegmentLeft[aNodeIndeciesLeft[0]].aPos[1]])
		# 			aMazeNodes[aSegmentLeft[aNodeIndeciesLeft[0]].aPos[0]][aSegmentLeft[aNodeIndeciesLeft[0]].aPos[1]].assignConnection("Left", aSegmentDown[aNodeIndeciesLeft[1].aPos])
		# 			aMazeNodes[aSegmentLeft[aNodeIndeciesLeft[1]].aPos[0]][aSegmentLeft[aNodeIndeciesLeft[1]].aPos[1]].assignConnection("Right", aSegmentDown[aNodeIndeciesLeft[0].aPos])

		# 			del aSegmentLeft[aNodeIndeciesLeft[0]:aNodeIndeciesLeft[1]]

		# 			aNodeIndeciesLeft.pop(0)
		# 			print(aNodeIndeciesLeft, aSegmentLeft)

		# 	if countNodes(aSegmentDown) >= 2 or countNodes(aSegmentLeft) >= 2:
		# 		makeConnectionDownLeft(aSegmentDown, aSegmentLeft)

		##-------------------------------------------------##
		def makeConnectionsHorizontal(aSegment):
			if countNodes(aSegment) >= 2:
				aNodeIndecies = []
				for i in range(len(aSegment)):
					if isinstance(aSegment[i], NODE):
						aNodeIndecies.append(i)

				if all(pos == 0 for pos in aSegment[aNodeIndecies[0] + 1:aNodeIndecies[1]]) or aSegment[aNodeIndecies[0] + 1:aNodeIndecies[1]] == []:
					aMazeNodes[aSegment[aNodeIndecies[0]].aPos[0]][aSegment[aNodeIndecies[0]].aPos[1]].assignConnection("Right", aSegment[aNodeIndecies[1]].aPos)
					aMazeNodes[aSegment[aNodeIndecies[1]].aPos[0]][aSegment[aNodeIndecies[1]].aPos[1]].assignConnection("Left", aSegment[aNodeIndecies[0]].aPos)

					aSegment[aNodeIndecies[0]] = 1

					# print(aSegment)
					# del aSegment[0:aNodeIndecies[1]]
					# print("Segment:", aSegment)

					aNodeIndecies.pop(0)

				elif countNodes(aSegment) <= 1:
					return

				try:
					if aSegment[aNodeIndecies[0] + 1] == 1:
						aSegment[aNodeIndecies[0]] = 1
						aNodeIndecies.pop(0)
				except IndexError:
					pass

			if countNodes(aSegment) >= 2:
				makeConnectionsHorizontal(aSegment)
		##-------------------------------------------------##


		##-------------------------------------------------##
		def makeConnectionsVertical(aSegment):
			if countNodes(aSegment) >= 2:
				aNodeIndecies = []
				for i in range(len(aSegment)):
					if isinstance(aSegment[i], NODE):
						aNodeIndecies.append(i)

				if all(pos == 0 for pos in aSegment[aNodeIndecies[0] + 1:aNodeIndecies[1]]) or aSegment[aNodeIndecies[0] + 1:aNodeIndecies[1]] == []:
					aMazeNodes[aSegment[aNodeIndecies[0]].aPos[0]][aSegment[aNodeIndecies[0]].aPos[1]].assignConnection("Down", aSegment[aNodeIndecies[1]].aPos)
					aMazeNodes[aSegment[aNodeIndecies[1]].aPos[0]][aSegment[aNodeIndecies[1]].aPos[1]].assignConnection("Up", aSegment[aNodeIndecies[0]].aPos)

					aSegment[aNodeIndecies[0]] = 1

					# print(aSegment)
					# del aSegment[0:aNodeIndecies[1]]
					# print("Segment:", aSegment)

					aNodeIndecies.pop(0)

				elif countNodes(aSegment) <= 1:
					return

				# if all(pos == 0 for pos in aSegment[aNodeIndecies[0] + 1:aNodeIndecies[1]]) == False:
				# 	print("yyay")
				# 	aSegment[aNodeIndecies[0]] = 1

				# 	aNodeIndecies.pop(0)

				try:
					if aSegment[aNodeIndecies[0] + 1] == 1:
						aSegment[aNodeIndecies[0]] = 1
						aNodeIndecies.pop(0)
				except IndexError:
					pass

			if countNodes(aSegment) >= 2:
				makeConnectionsVertical(aSegment)
		##-------------------------------------------------##

		aMazeNodes = copy.deepcopy(self.aMazeUnsolved)

		aStart, aEnd = self.findStartEnd()

		print("End:", aEnd)

		aMazeNodes[aStart[0]][aStart[1]] = NODE(aStart)
		aMazeNodes[aEnd[0]][aEnd[1]] = NODE(aEnd)

		for r in range(len(self.aMazeUnsolved)):
			for s in range(len(self.aMazeUnsolved[r])):
				if s != 0 and r != len(self.aMazeUnsolved) - 1: #--Ensures only checking withing the width of the maze
					if self.aMazeUnsolved[r][s] == 0:
						if self.aMazeUnsolved[r + 1][s] == 1 and self.aMazeUnsolved[r][s - 1] == 1 and self.aMazeUnsolved[r - 1][s] == 0 and self.aMazeUnsolved[r][s + 1] == 0: #--Check for down and turning right
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 1 and self.aMazeUnsolved[r][s - 1] == 0 and self.aMazeUnsolved[r - 1][s] == 0 and self.aMazeUnsolved[r][s + 1] == 1: #--Check for down and turning left
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 0 and self.aMazeUnsolved[r][s - 1] == 0 and self.aMazeUnsolved[r - 1][s] == 1 and self.aMazeUnsolved[r][s + 1] == 1: #--Check for up and turning left
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 0 and self.aMazeUnsolved[r][s - 1] == 1 and self.aMazeUnsolved[r - 1][s] == 1 and self.aMazeUnsolved[r][s + 1] == 0: #--Check for up and turning right
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 0 and self.aMazeUnsolved[r][s - 1] == 1 and self.aMazeUnsolved[r - 1][s] == 0 and self.aMazeUnsolved[r][s + 1] == 0: #--Check for t-junction left
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 0 and self.aMazeUnsolved[r][s - 1] == 0 and self.aMazeUnsolved[r - 1][s] == 0 and self.aMazeUnsolved[r][s + 1] == 1: #--Check for t-junction right
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 1 and self.aMazeUnsolved[r][s - 1] == 0 and self.aMazeUnsolved[r - 1][s] == 0 and self.aMazeUnsolved[r][s + 1] == 0: #--Check for t-junction up
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 0 and self.aMazeUnsolved[r][s - 1] == 0 and self.aMazeUnsolved[r - 1][s] == 1 and self.aMazeUnsolved[r][s + 1] == 0: #--Check for t-junction down
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 1 and self.aMazeUnsolved[r][s - 1] == 1 and self.aMazeUnsolved[r - 1][s] == 1 and self.aMazeUnsolved[r][s + 1] == 0: #--Check for dead end left
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 1 and self.aMazeUnsolved[r][s - 1] == 0 and self.aMazeUnsolved[r - 1][s] == 1 and self.aMazeUnsolved[r][s + 1] == 1: #--Check for dead end right
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 1 and self.aMazeUnsolved[r][s - 1] == 1 and self.aMazeUnsolved[r - 1][s] == 0 and self.aMazeUnsolved[r][s + 1] == 1: #--Check for dead end down
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 0 and self.aMazeUnsolved[r][s - 1] == 1 and self.aMazeUnsolved[r - 1][s] == 1 and self.aMazeUnsolved[r][s + 1] == 1: #--Check for dead end up
							aMazeNodes[r][s] = NODE([r, s])

						elif self.aMazeUnsolved[r + 1][s] == 0 and self.aMazeUnsolved[r][s - 1] == 0 and self.aMazeUnsolved[r - 1][s] == 0 and self.aMazeUnsolved[r][s + 1] == 0: #--Check for crossroad
							aMazeNodes[r][s] = NODE([r, s])

		for row in aMazeNodes:
			aSegment = copy.deepcopy(row)

			makeConnectionsHorizontal(aSegment)

		for j in range(len(aMazeNodes)):
			aSegment = []
			for row in aMazeNodes:
				aSegment.append(row[j])

			makeConnectionsVertical(aSegment)

		# aSegmentDown = []
		# for i in range(len(self.aMazeUnsolved)):
		# 	aSegmentDown.append(aMazeNodes[i][aMazeNodes[r][s].aPos[1]])

		# aSegmentLeft = []
		# for i in range(len(self.aMazeUnsolved)):
		# 	aSegmentLeft.append(aMazeNodes[aMazeNodes[r][s].aPos[0]][i])


		# print(aSegmentLeft)
		# print(aSegmentDown)

		# makeConnectionDownLeft(aSegmentDown, aSegmentLeft)

		return aMazeNodes

	def pathing(self, aMazeNodes, aStart, aEnd, vItteration = 0):
		aMazeNodesCopy = copy.deepcopy(aMazeNodes)

		print("\n", vItteration, "\n")

		# print(aMazeNodesCopy[0][1].aDown)

		aPatherCoords = copy.deepcopy(aStart)

		# if vItteration > 0:
		# 	for i in range(vItteration):
		# 		if aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aDown != []: #--If can go down, go down
		# 			aPastPatherCoords = copy.deepcopy(aPatherCoords)
		# 			aPatherCoords = aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aDown
		# 			aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]].assignConnection("Down", [])

		# 		elif aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aRight != []: #--If can go right, go right
		# 			aPastPatherCoords = copy.deepcopy(aPatherCoords)
		# 			aPatherCoords = aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aRight
		# 			aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]].assignConnection("Right", [])

		# 		elif aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aLeft != []: #--If can go left, go left
		# 			aPastPatherCoords = copy.deepcopy(aPatherCoords)
		# 			aPatherCoords = aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aLeft
		# 			aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]].assignConnection("Left", [])

		# 		elif aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aUp != []: #--If can go up, go up
		# 			aPastPatherCoords = copy.deepcopy(aPatherCoords)
		# 			aPatherCoords = aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aUp
		# 			aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]].assignConnection("Up", [])

		# 	aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]] = 0

		# 	self.displayMaze(aMazeNodesCopy)

		aPatherCoords = copy.deepcopy(aStart)

		vItteration += 1

		vRound = 0
		aCancelCheckOne = []
		aCancelCheckTwo = []

		vLastDir = ""
		aVisitedNodes = []

		vSolved = False
		while not(vSolved):

			print(aPatherCoords)

			# print("Prev:", aPatherCoords)

			if aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aDown != []: #--If can go down, go down
				aPastPatherCoords = copy.deepcopy(aPatherCoords)
				aPatherCoords = aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aDown
				aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]].assignConnection("Down", [])
				# aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]] = 0

			elif aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aRight != []: #--If can go right, go right
				aPastPatherCoords = copy.deepcopy(aPatherCoords)
				aPatherCoords = aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aRight
				aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]].assignConnection("Right", [])
				# aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]] = 0

			elif aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aLeft != []: #--If can go left, go left
				aPastPatherCoords = copy.deepcopy(aPatherCoords)
				aPatherCoords = aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aLeft
				aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]].assignConnection("Left", [])
				# aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]] = 0

			elif aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aUp != []: #--If can go up, go up
				aPastPatherCoords = copy.deepcopy(aPatherCoords)
				aPatherCoords = aMazeNodesCopy[aPatherCoords[0]][aPatherCoords[1]].aUp
				aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]].assignConnection("Up", [])
				# aMazeNodesCopy[aPastPatherCoords[0]][aPastPatherCoords[1]] = 0

			# print("Now:", aPatherCoords)

			# print("Past:", aPastPatherCoords)
			# print("Present:", aPatherCoords)


			if vRound % 2 == 0:
				aCancelCheckOne = copy.deepcopy(aPatherCoords)
			else:
				aCancelCheckTwo = copy.deepcopy(aPatherCoords)

			vRound += 1

			# print(aCancelCheckOne, aCancelCheckTwo, vRound)

			if aCancelCheckOne == aCancelCheckTwo:
				aVisitedNodes.append(aPatherCoords)
				print("")
				self.pathing(aMazeNodes, aStart, aEnd, vItteration)

			if aPatherCoords == aEnd:
				print("Solution Found")
				print("Visited Nodes:", aVisitedNodes)
				vSolved = True

		aSolvedMaze = copy.deepcopy(self.aMazeUnsolved)

		for coord in aVisitedNodes:
			aSolvedMaze[coord[0]][coord[1]] = 5

		return aSolvedMaze



	def main(self):
		aStart, aEnd = self.findStartEnd()
		print()
		self.displayMaze(self.aMazeUnsolved)
		aMazeNodes = self.createNodes()

		# print("Connection:", aMazeNodes[8][3].aDown)
		# print()
		# print("Connection:", aMazeNodes[1][5].aRight)

		# print("Connection:", aMazeNodes[1][7].aRight)

		self.displayMaze(aMazeNodes)

		aSolvedMaze = self.pathing(aMazeNodes, aStart, aEnd)

		print("Solution: ")
		self.displayMaze(aSolvedMaze)
		# self.writeMaze(self.aMazeUnsolved, aSolvedMaze)

maze = MAZE("../Mazes/20x20.png") #--Initilises an instance of the MAZE object with the path to the maze image
maze.main() #--Runs the main method


"""
LOOPS ARE FINE?

NOde connection issue????
vertical selectivly?????????????
"""