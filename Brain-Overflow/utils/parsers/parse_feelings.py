import json
def parse_feelings(body):
	x = json.loads(body)
	print('feelings:')
	print(x['timestamp'])

parse_feelings.field = 'feelings'