import json
from PIL import Image
from server import parser
import functools

server_supported_functions = {}

def get_supported_functions():
	return server_supported_functions

def parser(f_name):
    def decorator(f):
        server_supported_functions[f_name] = f
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
    return decorator

@parser('translation')
def parse_translation(context, snapshot):
	with open(context.directory / 'translation.json', 'w') as writer:
		translation = snapshot.translation
		data = {"x": translation[0], "y": translation[1], "z": translation[2]}
		json.dump(data, writer)

@parser('color_image')
def parse_color_image(context, snapshot):
	color_image = snapshot.color_image
	width = color_image[1]
	height = color_image[0]
	data = color_image[2]
	image = Image.new('RGB', (width, height))
	#TODO - see Gittik's comment: ex06,Decemeber 11, 3:44 pm 
	data_flat_pixel = [(data[i:i+3]) for i in range(0, len(data), 3)]
	image.putdata(data_flat_pixel)
	path = context.directory / 'color_image.jpeg'
	image.save(path)

