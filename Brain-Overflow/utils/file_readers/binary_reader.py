import struct 
import os
import datetime as dt
import click
from utils import protocol
from utils import user

class BinaryReader:
	def __init__(self, path):
		self.file = open(path, 'rb')

	def __str__(self):
		return 'BinaryReader of file: {0}'.format(str(file))

	def __repr__(self):
		#TODO 
		return 'reader = BinaryReader(path)\nreader.user\n '

	def process_file(self):
		#yield self.get_user_info(file)
		snapshots_gen = self.gen_snapshots()
		for s in snapshots_gen:
			yield s

	def get_user_info(self):
		user_id, user_name_size = BinaryReader.read_in_format(self.file, 'li')
		user_name, = BinaryReader.read_in_format(self.file,'{0}s'.format(user_name_size))
		user_name = user_name.decode()
		user_birth_date, user_gender = BinaryReader.read_in_format(self.file, 'ic')
		user_gender = user_gender.decode()

		return user.User(
			user_id,
			user_name,
			user_birth_date,
			user_gender)

	def construct_snapshot(self):
		timestamp, \
		translation_x, \
		translation_y, \
		translation_z, \
		rotation_x, \
		rotation_y, \
		rotation_z, \
		rotation_w, \
		color_image_width, \
		color_image_height = BinaryReader.read_in_format(self.file,'QdddddddII')
		translation = (translation_x, translation_y, translation_z)
		rotation = (rotation_x, rotation_y, rotation_z, rotation_w)
		
		color_image_size = color_image_width * color_image_height
		color_image_vals = self.file.read(3*color_image_size)
		color_image_vals = struct.unpack('{0}B'.format(color_image_size*3), color_image_vals)
		color_image_vals = BinaryReader.bgr_to_rgb(color_image_vals)
		color_image = (color_image_height, color_image_width, color_image_vals)

		depth_image_width, depth_image_height = BinaryReader.read_in_format(self.file, 'II')
		depth_image_size = depth_image_height * depth_image_width
		depth_image_vals = self.file.read(4*depth_image_size)
		depth_image = (depth_image_height, depth_image_width, depth_image_vals)

		user_feelings = BinaryReader.read_in_format(self.file, 'ffff')

		#TODO - change to reader_snapshot util
		return protocol.Snapshot(timestamp, translation, rotation, color_image, depth_image, user_feelings)

	def gen_snapshots(self):
		try:
			snapshot = self.construct_snapshot()
			while snapshot:
				yield snapshot
				snapshot = self.construct_snapshot()
		except Exception as e:
			print(e)
		finally:
			self.file.close()
			return 

##### Binary utilities #####
	def bgr_to_rgb(raw_img_bin):
		raw_img_bin = [raw_img_bin[i:i+3][::-1] for i in range(0, len(raw_img_bin), 3)]
		return [a for tup in raw_img_bin for a in tup]
		#x = struct.pack('{0}B'.format(len(raw_img_bin)), *raw_img_bin)
		#print(x[:1])
		#return x
		#return b''.join(raw_img_bin)

	def read_in_format(file, requested_format):
		bin_length = struct.calcsize(requested_format)
		var_bin_repr = file.read(bin_length)
		var_requested_repr = struct.unpack(requested_format, var_bin_repr)
		return var_requested_repr

BinaryReader.file_format = 'binary'





