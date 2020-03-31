from PIL import Image
from utils import context

def parse_color_image(snapshot):
	color_image_w, color_image_h, color_image_raw_path = snapshot['color_image']
	color_image_context = context.Context(snapshot['user_id'], snapshot['timestamp'], 'color_image')
	color_image_parsed_path = color_image_context.get_path('parsed.jpg')

	#TODO - remove file handling from the parser
	with open(color_image_raw_path, 'rb') as f:
		raw_image = f.read()

	size = (color_image_w , color_image_h)
	image = Image.frombytes('RGB' , size, raw_image)
	image.save(color_image_parsed_path)

parse_color_image.field = 'color_image'

