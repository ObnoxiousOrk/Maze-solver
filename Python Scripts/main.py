"""
Name: mazeSolver.py
Date Start: 24/3/2020
Date End: 

0 = Walkable
1 = Wall
2 = Start
3 = End
8 = Path
"""

import copy
import numpy as np
from PIL import Image

class MAZE():
	def __init__(self, maze):
		self.aMazeUnsolved = self.getMaze(maze) #--Initilises the instance variable in the array with the value returned from the getMaze function

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
			print(row)

	def findStartEnd(self):
		for i in range(len(self.aMazeUnsolved[0])):
			if self.aMazeUnsolved[0][i] == 0: #--If the pixel that is being interrogated on the top line is walkable, it has to be the start, so set it to the start character
				self.aMazeUnsolved[0][i] = 2
				vStart = [0, i]

		for i in range(len(self.aMazeUnsolved[len(self.aMazeUnsolved)-1])):
			if self.aMazeUnsolved[len(self.aMazeUnsolved)-1][i] == 0: #--If the pixel that is being interrogated on the last line is walkable, it has to be the end, so set it to the end character
				self.aMazeUnsolved[len(self.aMazeUnsolved)-1][i] = 3
				vEnd = [len(self.aMazeUnsolved)-1, i]

		return vStart, vEnd #--Returns the coords of the start and the end as an array [y, x] from the top left

	def pathing(self, vStart, vEnd):
		aMazeWIP = copy.deepcopy(self.aMazeUnsolved) #--Copys the maze from the stored, unsolved maze, to a new variable so that changes can be made and the origional can be kept
		aMazeWIPChanges = copy.deepcopy(aMazeWIP)

		aMazeSolution = copy.deepcopy(self.aMazeUnsolved)

		vPatherCoords = copy.deepcopy(vStart) #--Tells the pather to start pathing at the maze entrance

		vSolved = False

		while not(vSolved):
			aMazeWIP[vPatherCoords[0]][vPatherCoords[1]] = 8 #--Sets the value of the coord that the pather is at to 8 so that it doesnt end up backtracking

			if aMazeWIP[vPatherCoords[0] + 1][vPatherCoords[1]] == 0: #--If there is a walkable space below the pather, it should move down
				vPatherCoords[0] += 1

			elif aMazeWIP[vPatherCoords[0] + 1][vPatherCoords[1]] == 3: #--if going down to the exit (will always be down - maze exit is on bottom row)
				vSolved = True
				aMazeSolution = copy.deepcopy(aMazeWIP) #--Copys the solved maze to a variable called solved maze so I don't get confused
				print("Maze Solved")


			elif aMazeWIP[vPatherCoords[0]][vPatherCoords[1] - 1] == 0: #--If there is a walkable space to the left of the pather, it should move left
				vPatherCoords[1] -= 1

			elif aMazeWIP[vPatherCoords[0]][vPatherCoords[1] + 1] == 0: #--If there is a walkable space to the right of the pather, it should move right
				vPatherCoords[1] += 1

			elif aMazeWIP[vPatherCoords[0] - 1][vPatherCoords[1]] == 0: #--If there is a walkable space above the pather, it should move up
				vPatherCoords[0] -= 1

			else: #--If there are no valid moved, the space the pather is on shoudl be marked as a wall, the maze should be copied, and the pather should start again
				vStuckCoords = vPatherCoords
				aMazeWIP = copy.deepcopy(aMazeWIPChanges)
				vPatherCoords = copy.deepcopy(vStart)
				aMazeWIP[vStuckCoords[0]][vStuckCoords[1]] = 1
				aMazeWIPChanges = copy.deepcopy(aMazeWIP)


		return aMazeSolution

	def writeMaze(self, aMaze, aMazeSolution):
		#--Gets the maze width and height
		w = len(aMaze[0])
		h = len(aMaze)

		data = np.zeros((h, w, 3), dtype=np.uint8) #--Creates a 3D array 3 deep with the length and width of the maze and fills it with 0s

		for r in range(len(aMaze)):
			for p in range(len(aMaze[r])):
				#--For each space in the maze, get the value and assign each pixel an RGB value based on the value
				if aMaze[r][p] == 0 and aMazeSolution[r][p] != 8:
					data[r][p] = [255, 255, 255] #--RGB value to be written and coords to be written to

				elif aMaze[r][p] == 1:
					data[r][p] = [0, 0, 0] 

				elif aMaze[r][p] == 2:
					data[r][p] = [0, 255, 0]

				elif aMaze[r][p] == 3:
					data[r][p] = [255, 0, 0]

				else:
					data[r][p] = [0, 0, 255]

		img = Image.fromarray(data, "RGB") #--Construts an image from the array of RGB colour values
		img.save("solvedMaze.png") #--Saves the image as solvedMaze.png
		# img.show() #--Shows the image

	def main(self):
		vStart, vEnd = self.findStartEnd()
		self.displayMaze(self.aMazeUnsolved)
		aSolvedMaze = self.pathing(vStart, vEnd)

		print("Solution: ")
		self.displayMaze(aSolvedMaze)
		self.writeMaze(self.aMazeUnsolved, aSolvedMaze)

maze = MAZE("../Mazes/MazeImproved.png") #--Initilises an instance of the MAZE object with the path to the maze image
maze.main() #--Runs the main method