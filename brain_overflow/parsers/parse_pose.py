

def parse_pose(snapshot): 
	return {
	'translation' : snapshot['pose']['translation'],
	'rotation' : snapshot['pose']['rotation']	
	}
	
#parse_pose.field = ('translation', 'rotation')
parse_pose.field = 'pose'