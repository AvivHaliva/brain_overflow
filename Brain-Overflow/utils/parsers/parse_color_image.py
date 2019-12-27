from PIL import Image

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

parse_color_image.field = 'color_image'