from cortex_pb2 import User, Snapshot
import struct
import gzip
from utils import user

#TODO - make compatiable with the rest of the code
class ProtobufReader:
	def __init__(self, path):
		self.file = gzip.open(path, "rb") 
		
	def get_user_info(self):
		user_message_len_bin = self.file.read(struct.calcsize('I'))
		self.offset = struct.calcsize('I')
		user_message_len = struct.unpack('I', user_message_len_bin)[0]
		user_message = self.file.read(user_message_len)
		u = User()
		u.ParseFromString(user_message)
		#TODO handle gender
		return user.User(u.user_id, u.username, u.birthday, u.gender)

	def process_file(self):
		for s in self.gen_snapshots():
			yield s

	def get_next_message(self):
		#TODO - maybe user BinaryREader.read_in_format??
		message_len_bin = self.file.read(struct.calcsize('I'))
		message_len = struct.unpack('I', message_len_bin)[0]
		message = self.file.read(message_len)
		return message


	def gen_snapshots(self):
		try:
			message = self.get_next_message()
			while message:
				snapshot = Snapshot()
				snapshot.ParseFromString(message)
				yield (snapshot.datetime, snapshot.pose.translation, snapshot.pose.rotation, snapshot.color_image, snapshot.depth_image, snapshot.feelings)
				message = self.get_next_message()
		except Exception as e:
			print(e)
		finally:
			self.file.close()
			return
		
ProtobufReader.file_format = 'protobuf'