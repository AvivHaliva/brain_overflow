import click
from ..mq import MessageQueue
from .saver import Saver

@click.command()
@click.argument("db_url")
@click.argument("topic")
@click.argument("data_to_save")
def save(db_url, topic, data_to_save):
	saver = Saver(db_url)
	saver.save(topic, data_to_save)

@click.command('run-saver')
@click.argument("db_url")
@click.argument("message_queue_url")
def run_saver(db_url, message_queue_url):
	mq = MessageQueue(message_queue_url)
	mq.declare_topic_exchange('snapshots_parsed')
	mq.declare_queue('saver')
	mq.bind_queue_to_exchange('saver', 'snapshots_parsed', '#')

	saver = Saver(db_url)
	mq.consume_from_queue('saver', saver.callback)
