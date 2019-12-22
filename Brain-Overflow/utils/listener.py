from utils import Connection
import socket

class Listener:
	def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
		self.port = port
		self.host = host
		self.backlog = backlog
		self.reuseaddr = reuseaddr
		self.server = None

    #managed context
	def __enter__(self):
		self.start()
		return self

	def __exit__ (self, exception, error, traceback):
		self.stop()

	def __repr__(self):
		return f'Listener(port={self.port!r}, host={self.host!r}, backlog={self.backlog!r}, reuseaddr={self.reuseaddr!r})'

	def start(self):
		self.server = socket.socket()
		# reuse address
		if self.reuseaddr:
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# pass tuple of ip and port
		self.server.bind((self.host, self.port))
		# listen on the ip and port
		self.server.listen(self.backlog)

	def stop(self):
		self.server.close()

	def accept(self):
		# create a socket for the specific connection and return it
		client, address = self.server.accept()
		return Connection(client)
