import json

def parse_translation(body):
	
	#TODO - change to x = snapshot.pose.translation.x
	#context.save('translation.json', json.dumps(dict(
    #	x = snapshot.translation[0],
    #	y = snapshot.translation[1],
    #	z = snapshot.translation[2],
    #	)))
	x = json.loads(body)
	print('translation:')
	print(x['timestamp'])

parse_translation.field = 'translation'

