from PIL import Image
import numpy as np

def writeImage(aMaze, aMazeSolution):
	w = len(aMaze[0])
	h = len(aMaze)

	data = np.zeros((h, w, 3), dtype=np.uint8)

	for r in range(len(aMaze)):
		for p in range(len(aMaze[r])):
			print(aMaze[r][p])
			if aMaze[r][p] == 0 and aMazeSolution[r][p] != 8:
				data[r][p] = [255, 255, 255]

			elif aMaze[r][p] == 1:
				data[r][p] = [0, 0, 0] #--RGB value to be written and coords to be written to

			elif aMaze[r][p] == 2:
				data[r][p] = [0, 255, 0]

			elif aMaze[r][p] == 3:
				data[r][p] = [255, 0, 0]

			else:
				data[r, p] = [0, 0, 255]

	print(data)
	print(data.shape)

	img = Image.fromarray(data, 'RGB')
	img.save('my.png')
	img.show()