import pathlib
import importlib
import sys
import click
from mq import MessageQueue
import json

class Parser:
	def __init__(self):
		self.supported_parsers = {}
		self.load_parsers('/home/user/Brain-Overflow/Brain-Overflow/parsers/')

	def load_parsers(self, root):
		root = pathlib.Path(root).absolute()
		sys.path.insert(0, str(root.parent))
		for path in root.iterdir():
			if path.name.startswith('parse_') and path.suffix == '.py':
				m = importlib.import_module(f'{root.name}.{path.stem}', package=root.name)
				for f in dir(m):
					if f.startswith('parse_'):
						try:
							parse_f = getattr(m, f)
							self.supported_parsers[parse_f.field] = parse_f
						except:
							pass


def run_parser(parser_name, data):
	parserManager = Parser()
	p = parserManager.supported_parsers[parser_name]
	if p is None:
		return
	return p(data)


@click.command('run-parser')
@click.argument('parser_name')
@click.argument('message_queue_url')
def run_parser_command(parser_name, message_queue_url):
	parserManager = Parser()
	p = parserManager.supported_parsers[parser_name]
	if p is None:
		return

	mq = MessageQueue(message_queue_url)
	mq.declare_topic_exchange('snapshots_raw')
	mq.declare_queue(parser_name)
	routing_key = parser_name +'.raw'
	mq.bind_queue_to_exchange(parser_name, 'snapshots_raw', routing_key)

	def callback(ch, method, properties, body):
		recieved_message = json.loads(body)
		parser_res = p(recieved_message)
		routing_key = parser_name + '.parsed'
		mq.declare_topic_exchange('snapshots_parsed')

		if parser_name != 'user_info':
			message = {'parser_name': parser_name,
				'data': {'user_id': recieved_message['user_id'],
			 	'timestamp': recieved_message['timestamp'], 
			 	parser_name : parser_res}
			 }
		else:
			message =  {'parser_name': parser_name,
				'data': { parser_name : parser_res}}

		mq.publish_to_queue('snapshots_parsed', routing_key , json.dumps(message))

	mq.consume_from_queue(parser_name, callback)

@click.command('parse')
@click.argument('parser_name')
@click.argument('input_path')
def parse(parser_name, input_path):
	parserManager = Parser()	
	p = parserManager.supported_parsers[parser_name]
	if p is None:
		return	
	with open(input_path, 'r') as f:
		data = f.read()
		res = p(data)
		print(res)