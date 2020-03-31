from .protobuf_sample_format_pb2 import User, Snapshot
#TODO rename cortex_pb2
import struct
import gzip
from utils import user
from utils import protocol

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
				yield protocol.Snapshot(
					snapshot.datetime,
					(snapshot.pose.translation.x, snapshot.pose.translation.y, snapshot.pose.translation.z),
					(snapshot.pose.rotation.x, snapshot.pose.rotation.y, snapshot.pose.rotation.z, snapshot.pose.rotation.w),
					(snapshot.color_image.width, snapshot.color_image.height, snapshot.color_image.data),
					(snapshot.depth_image.width, snapshot.depth_image.height, snapshot.depth_image.data),
					(snapshot.feelings.hunger, snapshot.feelings.thirst, snapshot.feelings.exhaustion, snapshot.feelings.happiness))
				message = self.get_next_message()
		except Exception as e:
			#TODO improve error handling
			print(e)
		finally:
			self.file.close()
			return
		
ProtobufReader.file_format = 'protobuf'