import struct 
import os
import datetime as dt
import click
from utils import protocol

USER_ID_BYTES_SIZE = 8
USER_INFO_FIXED_SIZE = 17
SNAPSHOT_FORMAT = 'ldddddddII'

class Reader:
	def __init__(self, path):
		self.path = path
		self.offset = 0
		with open(self.path, "rb") as file:
			self.extract_user_info(file)

	def __str__(self):
		#TODO - create a dict instead {'m':'male', 'f':'female'} etc.
		gender = 'other'
		if self.user_gender == 'f':
			gender = 'female'
		elif self.user_gender == 'm':
			gender = 'male'
		return 'user {0}: {1}, born {2} ({3})'.format(self.user_id, self.user_name,dt.datetime.fromtimestamp(self.user_birth_date/1000.0).strftime('%d %B %Y'), gender)
	
	def __repr__(self):
		#TODO
		return 'reader = Reader(PATH)'

	def __iter__(self):
		with open(self.path, "rb") as file:
			for snapshot in self.process_snapshots(file):
				yield snapshot

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
		self.offset = USER_INFO_FIXED_SIZE + user_name_size

	def gen_next_snapshot_ts(self, file):
		file.seek(self.offset)
		try:
			data = self.read_var_in_requested_format(file, 8, 'Q')
			while data:
				yield data
				data = self.read_var_in_requested_format(file, 8, 'Q')
		finally:
			return

	def bgr_to_rgb(raw_img_bin):
		raw_img_bin = [raw_img_bin[i:i+3][::-1] for i in range(0, len(raw_img_bin), 3)]
		return b''.join(raw_img_bin)

	def process_snapshots(self, file):
		ts_gen = self.gen_next_snapshot_ts(file)
		for ts in ts_gen:
			translation = self.read_var_in_requested_format(file, 24, 'ddd')
			rotation = self.read_var_in_requested_format(file, 32, 'dddd')
			color_image_dimension = self.read_var_in_requested_format(file,8, 'II')
			color_image_size = color_image_dimension[0] * color_image_dimension[1]
			color_image_vals = file.read(color_image_size*3)
			color_image_vals = Reader.bgr_to_rgb(color_image_vals)
			color_image = (*color_image_dimension, color_image_vals)

			depth_image_dimension = self.read_var_in_requested_format(file,8, 'II')
			depth_image_size = depth_image_dimension[0] * depth_image_dimension[1]
			depth_image_vals = file.read(depth_image_size*4)
			depth_image_vals = Reader.bgr_to_rgb(depth_image_vals)
			depth_image = (*depth_image_dimension, depth_image_vals)

			user_feelings = self.read_var_in_requested_format(file, 4*4, 'ffff')
			
			yield protocol.Snapshot(ts, translation, rotation, color_image, depth_image, user_feelings)

@click.command()
@click.argument("path")
def read(path):
	reader = Reader(path)
	print(reader)
	for snapshot in reader:
		print(snapshot)


