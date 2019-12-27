import json

def parse_translation(context, snapshot):
	with open(context.directory / 'translation.json', 'w') as writer:
		translation = snapshot.translation
		data = {"x": translation[0], "y": translation[1], "z": translation[2]}
		json.dump(data, writer)

parse_translation.field = 'translation'
