

def parse_pose(snapshot):
	return {
	'translation' : snapshot['translation'],
	'rotation' : snapshot['rotation']
	}
	
#parse_pose.field = ('translation', 'rotation')
parse_pose.field = 'translation'