from PIL import Image
import numpy as np

def getMaze(source="Maze.png"):
	img = Image.open(source).convert("LA")
	aMaze = np.array(img)

	aBoolMaze = []

	for row in aMaze:
		aRow = []
		for pixel in row:
			if pixel[0] == 0:
				aRow.append(1)
			else:
				aRow.append(0)

		aBoolMaze.append(aRow)


	return aBoolMaze