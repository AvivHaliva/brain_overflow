import json

def parse_translation(context, snapshot):
	#TODO - change to x = snapshot.pose.translation.x
	context.save('translation.json', json.dumps(dict(
    	x = snapshot.translation[0],
    	y = snapshot.translation[1],
    	z = snapshot.translation[2],
    	)))		

parse_translation.field = 'translation'

