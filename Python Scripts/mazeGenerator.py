from PIL import Image
from random import randint

vSize = 10

aMazeData = [[0]*vSize]*vSize

def displayMaze(maze):
	for row in maze:
		print(row)

def chooseStart(size):
	vStartX = randint(0, size-1)

	return [0, vStartX]

vStart = chooseStart(vSize)

print(vStart)

def findPath(size, start):
	vPatherCoords = start
	aPath = []

	print(size)

	for r in range(size):
		for p in range(size):
			print(r, p)
			print(vPatherCoords)

			vDir = randint(1, 4)
			print(vDir)
			if [r, p] == vPatherCoords:
				if vDir == 1: #--Down
					aPath.append([r, p])
					vPatherCoords[r] += 1

				elif vDir == 2 and r != 0 and p != 0: #--Left
					aPath.append([r, p])
					vPatherCoords[p] += 1

				elif vDir == 3 and r != 0 and p != size-1: #-Right
					aPath.append([r, p])
					vPatherCoords[p] -= 1

				else: #--Up
					aPath.append([r, p])
					vPatherCoords[r] -= 1

			print(aPath)

findPath(vSize, vStart)



displayMaze(aMazeData)