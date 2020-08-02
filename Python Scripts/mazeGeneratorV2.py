from PIL import Image
from random import randint as rand

def displayMaze(maze):
	for row in maze:
		print(row)

# vWidth, vHeight = input("What size should the maze be (width, height)")  --Proper

vWidth, vHeight = 10, 10  #--used cos sublimes a lil bish

aMazeData = [[0]*vWidth]*vHeight

aStart = [0, rand(1, vWidth-2)]
aEnd = [vHeight-1, rand(1, vWidth-2)]

print(aStart, aEnd)

# aMazeData[aStart[0]][aStart[1]] = 2
# aMazeData[aEnd[0]][aEnd[1]] = 3

aMazeData[0][6] = 2
aMazeData[9][7] = 3

print(aMazeData)