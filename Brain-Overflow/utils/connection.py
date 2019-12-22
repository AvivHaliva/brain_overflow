import socket
import struct

INCOMPLETE_MESSAGE_ERR = 'incomplete message'
MESSAGE_SIZE_FORMAT = 'I'
MESSAGE_DATA_FORMAT = '{0}s'

class Connection:
    def __init__(self, socket):
    	self.socket = socket

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

    def send_message(self, data):
        data_size = len(data)
        data_format = MESSAGE_DATA_FORMAT.format(data_size)
        message_format = MESSAGE_SIZE_FORMAT + data_format
        message = struct.pack(message_format, data_size, data)
        self.send(message)

    def receive(self, size):
    	# receive <size> bytes or raise an exception
    	data = bytearray()
    	while len(data) < size:
            #import pdb;pdb.set_trace()
            packet = self.socket.recv(size - len(data))
            #import pdb;pdb.set_trace()
            if not packet:
                raise Exception(INCOMPLETE_MESSAGE_ERR)
            data.extend(packet)
    	return data

    def receive_message(self):
        data_size_bin = self.receive(struct.calcsize(MESSAGE_SIZE_FORMAT))
        data_size = struct.unpack(MESSAGE_SIZE_FORMAT, data_size_bin)[0]
        data_bin = self.receive(data_size)
        data = struct.unpack(MESSAGE_DATA_FORMAT.format(data_size), data_bin)
        return data[0]

    def close(self):
    	# close the socket
    	self.socket.close()



