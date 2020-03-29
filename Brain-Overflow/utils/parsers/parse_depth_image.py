from matplotlib import pyplot as plt
import numpy as np

# def parse_depth_image(context, snapshot):
# 	try:
# 		data = snapshot.depth_image[2]
# 		rows = snapshot.depth_image[0]
# 		cols = snapshot.depth_image[1]
# 		matrix = np.reshape(data, (rows, cols))
# 		plt.imshow(matrix, cmap=plt.cm.RdBu)
# 		path = context.path('depth_image.png')
# 		plt.savefig(path)
# 	except Exception as e:
# 		print('error in depth_image in :')
# 		print(snapshot.timestamp)

def parse_depth_image(body):
	x = json.loads(body)
	print('depth image')
	print(x['timestamp'])

parse_depth_image.field = 'depth_image'


'''

A depth image is a width × height array of floats, 
where each float represents how far the nearest surface from me was,
 in meters. 
 So, if I'd be looking at a chair, 
 the depth of its outline would be its proximity to me 
 (for example, 0.5 for half a meter), 
 and the wall behind it would be farther 
 (for example, 1.0 for one meter).
The best (2D) way to represent it is using matplotlib's heatmap.
'''