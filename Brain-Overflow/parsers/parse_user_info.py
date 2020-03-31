
def parse_user_info(data):
	return {
		'user_id': data['user_id'],
        'user_name': data['user_name'],
        'birthday': data['birthday'],
        'gender': data['gender']
	}

parse_user_info.field = 'user_info'

