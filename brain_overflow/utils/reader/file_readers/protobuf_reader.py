from utils.formats.protobuf_sample import User, Snapshot
import utils.formats.client_server_communication as client_server_communication_encoder
import struct
import gzip

class ProtobufReader:
	def __init__(self, path):
		self.file = gzip.open(path, "rb")
		
	def get_user_info(self):
		user_message_len_bin = self.file.read(struct.calcsize('I'))
		self.offset = struct.calcsize('I')
		user_message_len = struct.unpack('I', user_message_len_bin)[0]
		user_message = self.file.read(user_message_len)
		sample_user = User()
		sample_user.ParseFromString(user_message)

		return client_server_communication_encoder.gen_formatted_user(
			sample_user.user_id,
			sample_user.username,
			sample_user.birthday,
			sample_user.gender
			)

	def get_next_message(self):
		#TODO - maybe user BinaryREader.read_in_format??
		message_len_bin = self.file.read(struct.calcsize('I'))
		message_len = struct.unpack('I', message_len_bin)[0]
		message = self.file.read(message_len)
		return message

	@staticmethod
	def construct_snapshot(message):
		sample_snapshot = Snapshot()
		try:
			sample_snapshot.ParseFromString(message)
			return client_server_communication_encoder.gen_formatted_snapshot(
				sample_snapshot.datetime,
				sample_snapshot.pose.translation.x,
				sample_snapshot.pose.translation.y,
				sample_snapshot.pose.translation.z,
				sample_snapshot.pose.rotation.x,
				sample_snapshot.pose.rotation.y,
				sample_snapshot.pose.rotation.z,
				sample_snapshot.pose.rotation.w,
				sample_snapshot.color_image.width,
				sample_snapshot.color_image.height,
				sample_snapshot.color_image.data,
				sample_snapshot.depth_image.width,
				sample_snapshot.depth_image.height,
				list(sample_snapshot.depth_image.data),
				sample_snapshot.feelings.hunger,
				sample_snapshot.feelings.thirst,
				sample_snapshot.feelings.exhaustion,
				sample_snapshot.feelings.happiness
				)
		except Exception as e:
			pass

	def get_next_snapshot(self):
		try:
			message = self.get_next_message()
			return ProtobufReader.construct_snapshot(message)
		except Exception as e:
			pass
			
		
ProtobufReader.file_format = 'protobuf'