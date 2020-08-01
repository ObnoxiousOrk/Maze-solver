from PIL import Image
import numpy as np
import os

w, h = 10, 3
data = np.zeros((h, w, 3), dtype=np.uint8)

aPicData = [[1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 3, 1],]

aPicData2 =[[1, 8, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 8, 8, 8, 8, 8, 8, 8, 8, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 3, 1]]

def writeImage(aPicData, aPicData2):
	for r in range(len(aPicData)):
		for p in range(len(aPicData[r])):
			print(aPicData[r][p])
			if aPicData[r][p] == 0 and aPicData2[r][p] != 8:
				data[r][p] = [255, 255, 255]

			elif aPicData[r][p] == 1:
				data[r][p] = [0, 0, 0] #--RGB value to be written and coords to be written to

			elif aPicData[r][p] == 2:
				data[r][p] = [255, 0, 0]

			elif aPicData[r][p] == 3:
				data[r][p] = [0, 255, 0]

			else:# aPicData2[r][p] == 8:
				data[r, p] = [0, 0, 255]

	print(data)
	print(data.shape)

	img = Image.fromarray(data, 'RGB')
	img.save('my.png')
	img.show()

writeImage(aPicData, aPicData2)