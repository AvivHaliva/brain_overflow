import json
def parse_feelings(snapshot):
	hunger, thirst, exhaustion, happiness = snapshot['feelings']
	return {'hunger': hunger, 
			'thirst': thirst, 
			'exhaustion' : exhaustion,
			'happiness' : happiness}

parse_feelings.field = 'feelings'