import pathlib
import importlib
import sys
import click
from mq import MessageQueue
from utils.formats.parsers_message import gen_parser_input_message, gen_parser_output_message

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
	#TODO - run parse only if its fields are supported?
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
		input = gen_parser_input_message(body)
		parser_res = p(input)
		routing_key = parser_name + '.parsed'
		mq.declare_topic_exchange('snapshots_parsed')
		message = gen_parser_output_message(input, parser_name, parser_res)
		mq.publish_to_queue('snapshots_parsed', routing_key , message)

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