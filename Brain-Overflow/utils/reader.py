import struct 
import os

USER_ID_BYTES_SIZE = 8
SNAPSHOT_FORMAT = 'ldddddddII'

class Reader:
	def __init__(self, path):
		self.path = path
		with open(self.path, "rb") as file:
			self.extract_user_info(file)
			print(os.stat(path).st_size)
			self.process_snapshots(file)

	def read_var_in_requested_format(self, file, bin_length, requested_format, decode=False):
		var_bin_rep = file.read(bin_length)
		var_requested_rep = struct.unpack(requested_format, var_bin_rep)
		if len(var_requested_rep) < 2:
			var_requested_rep = var_requested_rep[0]
		if decode:
			var_requested_rep = var_requested_rep.decode()
		return var_requested_rep

	def extract_user_info(self, file):
		self.user_id = self.read_var_in_requested_format(file, USER_ID_BYTES_SIZE, 'l')
		user_name_size = self.read_var_in_requested_format(file, 4, 'i')
		self.user_name = self.read_var_in_requested_format(file, user_name_size, '{0}s'.format(user_name_size), True)
		self.user_birth_date = self.read_var_in_requested_format(file, 4, 'i')
		self.user_gender = self.read_var_in_requested_format(file, 1, 'c', True)

	def gen_next_snapshot_ts(self, file):
		data = self.read_var_in_requested_format(file, 8, 'l')
		while data:
			yield data
			data = self.read_var_in_requested_format(file, 8, 'l')
		return

	def process_snapshots(self, file):
		ts_gen = self.gen_next_snapshot_ts(file)
		for ts in ts_gen:
			print('gen next')
			translation = self.read_var_in_requested_format(file, 24, 'ddd')
			rotation = self.read_var_in_requested_format(file, 32, 'dddd')

			color_image_dimension = self.read_var_in_requested_format(file,8, 'II')
			color_image_size = color_image_dimension[0] * color_image_dimension[1]
			file.seek(color_image_size*3)
			#color_image_vals = file.read(color_image_size*3)
			depth_image_dimension = self.read_var_in_requested_format(file,8, 'II')
			depth_image_size = depth_image_dimension[0] * depth_image_dimension[1]
			#Memory error problem:
			#should unpack to floats somehow!
			#depth_image_vals = self.read_var_in_requested_format(file, depth_image_size, '{0}f'.format(depth_image_size))
			#depth_image_vals = file.read(depth_image_size)
			file.seek(depth_image_size)
			user_feelings = self.read_var_in_requested_format(file, 4*4, 'ffff')
			#Create snapshot object?
			print ('-------------')
			print(file.tell())

x = Reader('sample.mind')

