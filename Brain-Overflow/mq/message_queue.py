from .rabbitMQ import RabbitMQ
import furl


supported_mq_drivers = {'rabbitmq': RabbitMQ}

#TODO - maybe (?) create driver handler for both db and mq
# holds a diff dict for each type
# find driver gets url, driver category (db, mq...) 
def find_driver(url):
	for scheme, cls in supported_mq_drivers.items():
		if url.startswith(scheme):
			return cls
	raise ValueError(f'invalid url: {url}')

def initalize_driver(url):
	formatted_url = furl.furl(url)
	driver = find_driver(formatted_url.scheme)
	return driver(formatted_url.host, formatted_url.port)

class MessageQueue:
	def __init__(self, url):
		self.mq = initalize_driver(url)

	def declare_queue(self, queue_name):
		self.mq.declare_queue(queue_name)

	def declare_broadcast_queue(self, queue_name):
		self.mq.declare_broadcast_queue(queue_name)

	def publish_to_queue(self, queue_name, routing_key, message):
		self.mq.publish_to_queue(queue_name, routing_key, message)

	def bind_queue_to_exchange(self, queue_name, exchange_name):
		self.mq.bind_queue_to_exchange(queue_name, exchange_name)

	def consume_from_queue(self, queue_name, callback):
		self.mq.consume_from_queue(queue_name, callback)

	def close(self):
		self.mq.close()

