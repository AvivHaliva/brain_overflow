import socket

INCOMPLETE_MESSAGE_ERR = 'incomplete message'

class Connection:
    def __init__(self, socket):
    	self.socket = socket

    #managed context
    def __enter__(self):
    	return self

    def __exit__ (self, exception, error, traceback):
    	self.close()

    def __repr__(self):
    	src_ip = self.socket.getsockname()[0]
    	src_port = self.socket.getsockname()[1]
    	dest_ip = self.socket.getpeername()[0]
    	dest_port = self.socket.getpeername()[1]
    	return '<Connection from {0}:{1} to {2}:{3}>'.format(src_ip, src_port, dest_ip, dest_port)

    def connect(host, port):
    	#connects to the specified host and port, 
    	#and returns a Connection object for this connection.
    	conn = socket.socket()
    	address = (host, port)
    	conn.connect(address)
    	return Connection(conn)

    def send(self, data):
    	# send all the data on the socket
    	self.socket.sendall(data)

    def receive(self, size):
    	# receive <size> bytes or raise an exception
    	data = bytearray()
    	while len(data) < size:
    		packet = self.socket.recv(size - len(data))
    		if not packet:
    			raise Exception(INCOMPLETE_MESSAGE_ERR)
    		data.extend(packet)
    	return data

    def close(self):
    	# close the socket
    	self.socket.close()


