from PIL import Image

def parse_color_image(context, snapshot):
	#TODO - change w and h order -> remove it from parser!
	color_image = snapshot.color_image
	width = color_image[1]
	height = color_image[0]
	data = color_image[2]

	path = context.path('color_image.jpg')
	#TODO - chnage to -> size = snapshot.color_image.width, snapshot.color_image.heigh
	size = width, height
	image = Image.frombytes('RGB', size, data)
	#TODO - see Gittik's comment: ex06,Decemeber 11, 3:44 pm
	#data_flat_pixel = [data[i:i+3] for i in range(0, len(data), 3)]
	#image.putdata(data_flat_pixel)
	#TODO - chnage to ->image.putdata(snapshot.color_image.data)
	image.save(path)

parse_color_image.field = 'color_image'

