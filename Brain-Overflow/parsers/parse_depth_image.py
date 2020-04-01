from matplotlib import pyplot as plt
import numpy as np
from utils import context
import struct

def parse_depth_image(snapshot):
	depth_image_w, depth_image_h, depth_image_raw_path = snapshot['depth_image']
	depth_image_context = context.Context(snapshot['user_id'], snapshot['timestamp'], 'depth_image')
	depth_image_parsed_path = depth_image_context.get_path('parsed.jpg')

	#TODO - remove file handling from the parser
	with open(depth_image_raw_path, 'rb') as f:
		data = struct.unpack('{0}f'.format(depth_image_w*depth_image_h), f.read())

	matrix = np.reshape(data, (depth_image_h, depth_image_w))
	plt.imshow(matrix, cmap=plt.cm.RdBu)
	plt.imshow(matrix, cmap='hot', interpolation='nearest')
	plt.savefig(depth_image_parsed_path)

parse_depth_image.field = 'depth_image'
