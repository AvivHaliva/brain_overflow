import struct 
import os
import datetime as dt
import click
from brain_overflow.utils.formats import client_server_communication as client_server_communication_encoder

class BinaryReader:
	def __init__(self, path):
		self.file = open(path, 'rb')

	def __str__(self):
		return 'BinaryReader of file: {0}'.format(str(file))

	def __repr__(self):
		#TODO 
		return 'reader = BinaryReader(path)\nreader.user\n '

	def get_user_info(self):
		user_id, user_name_size = BinaryReader.read_in_format(self.file, 'li')
		username, = BinaryReader.read_in_format(self.file,'{0}s'.format(user_name_size))
		username = username.decode()
		user_birthday, user_gender = BinaryReader.read_in_format(self.file, 'ic')
		user_gender = user_gender.decode()

		return client_server_communication_encoder.gen_formatted_user(
			user_id,
			username,
			user_birthday,
			user_gender
			)

	def construct_snapshot(self):
		datetime, \
		translation_x, \
		translation_y, \
		translation_z, \
		rotation_x, \
		rotation_y, \
		rotation_z, \
		rotation_w, \
		color_image_height, \
		color_image_width = BinaryReader.read_in_format(self.file,'QdddddddII')
		
		color_image_size = color_image_width * color_image_height
		color_image_vals = self.file.read(3*color_image_size)
		color_image_vals = struct.unpack('{0}B'.format(color_image_size*3), color_image_vals)
		color_image_vals = BinaryReader.bgr_to_rgb(color_image_vals)
		color_image_vals = struct.pack('{0}B'.format(color_image_size*3), *color_image_vals)

		depth_image_height, depth_image_width = BinaryReader.read_in_format(self.file, 'II')
		depth_image_size = depth_image_height * depth_image_width
		depth_image_vals_raw = self.file.read(4*depth_image_size)
		depth_image_vals = struct.unpack('{0}f'.format(depth_image_size), depth_image_vals_raw)

		user_feelings = BinaryReader.read_in_format(self.file, 'ffff')

		return client_server_communication_encoder.gen_formatted_snapshot(
		datetime,
		translation_x, 
		translation_y, 
		translation_z, 
		rotation_x, 
		rotation_y, 
		rotation_z, 
		rotation_w, 
		color_image_width, 
		color_image_height,
		color_image_vals,
		depth_image_width,
		depth_image_height,
		depth_image_vals,
		*user_feelings
		)

	def get_next_snapshot(self):
 		return self.construct_snapshot()

##### Binary utilities #####
	def bgr_to_rgb(raw_img_bin):
		raw_img_bin = [raw_img_bin[i:i+3][::-1] for i in range(0, len(raw_img_bin), 3)]
		res = [a for tup in raw_img_bin for a in tup]
		return res
		#return struct.pack('{0}B'.format(len(res)), *res)

	def read_in_format(file, requested_format):
		bin_length = struct.calcsize(requested_format)
		var_bin_repr = file.read(bin_length)
		var_requested_repr = struct.unpack(requested_format, var_bin_repr)
		return var_requested_repr

BinaryReader.file_format = 'binary'





