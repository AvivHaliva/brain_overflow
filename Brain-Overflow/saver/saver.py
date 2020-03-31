import click
from db import DataBase
from db import DataBase
import json

class Saver:
	def __init__(self, db_url):
		self.db = DataBase(db_url)

	def save(self, topic, data):
		if topic == 'user_info':
			self.db.save_user(data)
		else:
			self.db.save_snapshot_data(data)

	def callback(self, ch, method, properties, body):
		message = json.loads(body)
		topic = message['parser_name']
		data = message['data']
		self.save(topic, data)
		import pdb; pdb.set_trace()



