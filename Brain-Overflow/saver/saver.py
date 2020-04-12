import click
from db import DataBase
from db import DataBase
import json

USER_INFO = 'user_info'
USER_ID = 'user_id'
PARSER_NAME = 'parser_name'

def gen_saving_user_format(message):
	user_info = message['user_info']
	user_info.update({USER_ID : message['user_id']})
	return user_info

def gen_saving_parser_res_format(message):
	parser_name = message['parser_name']
	return {
		USER_ID : message['user_id'],
		'snapshot_id' : message['snapshot_id'],
		'timestamp' : message['timestamp'],
		parser_name : message[parser_name]
	}

class Saver:
	def __init__(self, db_url):
		self.db = DataBase(db_url)

	def save(self, topic, data):
		if topic == 'user':
			self.db.save_user(data)
		else:
			self.db.save_snapshot_data(data)

	def callback(self, ch, method, properties, body):
		message = json.loads(body)
		# save user details #
		user_info = gen_saving_user_format(message)
		self. save('user', user_info)
		# save parser results #
		topic = message[PARSER_NAME]
		data = gen_saving_parser_res_format(message)
		self.save(topic, data)






