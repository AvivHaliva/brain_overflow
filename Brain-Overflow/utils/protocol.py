import struct
import datetime as dt
from utils import connection

HELLO_MESSAGE_FORMAT_1 = 'QI'
HELLO_MESSAGE_FORMAT_2 = '{0}sIc'
SNAPSHOT_MESSAGE_FORMAT_0 = 'Q3d4dIIII4f'
SNAPSHOT_MESSAGE_FORMAT_1 = 'Q3d4dII{0}BII4f'
SNAPSHOT_MESSAGE_FORMAT_2 = 'Q3d4dIIII{0}f4f'
SNAPSHOT_MESSAGE_FORMAT_3 = 'Q3d4dII{0}BII{1}f4f'

class Hello:
	def __init__(self, user_id, user_name, user_birth_date, user_gender):
		self.user_id = user_id
		self.user_name = user_name
		self.user_birth_date = user_birth_date
		self.user_gender = user_gender

	def __str__(self):
		gender = 'other'
		if self.user_gender == 'f':
			gender = 'female'
		elif self.user_gender == 'm':
			gender = 'male'
		return 'Hello message from user {0}: {1}, born {2} ({3})'.format(self.user_id, self.user_name,dt.datetime.fromtimestamp(self.user_birth_date/1000.0).strftime('%d %B %Y'), gender)


	def serialize(self):
		user_name_len = len(self.user_name.encode())
		serialized_hello_message = struct.pack(HELLO_MESSAGE_FORMAT_1 + HELLO_MESSAGE_FORMAT_2.format(user_name_len),
			self.user_id, 
			user_name_len, 
			self.user_name.encode(), 
			self.user_birth_date,
			self.user_gender.encode())
		return serialized_hello_message

	def deserialize(data):
		user_id, user_name_size_bin = struct.unpack(HELLO_MESSAGE_FORMAT_1, data[:struct.calcsize(HELLO_MESSAGE_FORMAT_1)])
		user_name_bin, birth_date, gender_bin = struct.unpack_from(HELLO_MESSAGE_FORMAT_2.format(user_name_size_bin), data, struct.calcsize(HELLO_MESSAGE_FORMAT_1))
		user_name = user_name_bin.decode()
		gender = gender_bin.decode()
		return Hello(user_id, user_name, birth_date, gender)

class Config:
	def __init__(self, fields_num, fields):
		self.fields_num = fields_num
		self.fields = fields

	def __str__(self):
		return '{0} fields are supported: {1}'.format(self.fields_num, self.fields)

	def serialize(self):
		encoded_fields = [f.encode() for f in self.fields]
		encoded_fields_len = [len(f) for f in encoded_fields]
		config_format = 'I'
		data = [self.fields_num]
		for i in range(self.fields_num):
			config_format += 'I{0}s'.format(encoded_fields_len[i])
			data.append(encoded_fields_len[i])
			data.append(encoded_fields[i])
		serialized_config_message = struct.pack(config_format, *data)
		return serialized_config_message

	def deserialize(data):
		int_size = struct.calcsize('I')
		fields_num = struct.unpack_from('I', data)[0]
		fields = []
		offset = int_size
		for i in range(fields_num):
			# do not start unpacking int from a null byte
			# TODO - find a more elegant solution
			while data[offset] == 0:
				offset += 1
			curr_field_size = struct.unpack_from('I', data, offset)[0]
			offset += int_size
			curr_field = struct.unpack_from('{0}s'.format(curr_field_size),data, offset)[0]
			fields.append(curr_field.decode())
			offset += curr_field_size
		config_message = Config(fields_num, fields)
		return config_message

class Snapshot:
	def __init__(self, \
		ts, \
		translation=(0,0,0), \
		 rotation=(0,0,0,0), \
		  color_image=(0,0,None),\
		   depth_image=(0,0,None),\
		   user_feelings=(0,0,0,0)
		   ):
		self.timestamp = ts
		self.translation = translation
		self.rotation = rotation
		self.color_image = color_image
		self.depth_image = depth_image
		self.feelings = user_feelings

	def __str__(self):
		datetime = dt.datetime.fromtimestamp(self.timestamp/1000.0)
		ts = datetime.strftime('%d %B %Y')
		hour = datetime.strftime('%H:%M:%S')
		return 'Snapshot from {0} at {1} on {2} / {3} with a {4}x{5} color image and a {6}x{7} depth image.'.format(ts, hour, self.translation, self.rotation,self.color_image[1], self.color_image[0], self.depth_image[1], self.depth_image[0])

	def serialize(self):
		color_img_size = self.color_image[0]*self.color_image[1]
		depth_img_size = self.depth_image[0]*self.depth_image[1]
		if color_img_size == 0:
			if depth_img_size == 0:
				serialized_snapshot = struct.pack(SNAPSHOT_MESSAGE_FORMAT_0,self.timestamp, *self.translation, *self.rotation, self.color_image[0], self.color_image[1], self.depth_image[0], self.depth_image[1], *self.feelings)
			else:
				serialized_snapshot = struct.pack(SNAPSHOT_MESSAGE_FORMAT_2.format(depth_img_size),self.timestamp, *self.translation, *self.rotation,self.color_image[0], self.color_image[1], self.depth_image[0], self.depth_image[1], self.depth_image[2], *self.feelings)
		elif depth_img_size == 0:
			serialized_snapshot = struct.pack(SNAPSHOT_MESSAGE_FORMAT_1.format(color_img_size*3),self.timestamp, *self.translation, *self.rotation, self.color_image[0], self.color_image[1],*self.color_image[2], self.depth_image[0], self.depth_image[1], *self.feelings)
		else:
			serialized_snapshot = struct.pack(SNAPSHOT_MESSAGE_FORMAT_3.format(color_img_size*3, depth_img_size),self.timestamp, *self.translation, *self.rotation, self.color_image[0], self.color_image[1], *self.color_image[2],self.depth_image[0], self.depth_image[1], *self.depth_image[2], *self.feelings)
		return serialized_snapshot

	def deserialize(data):
		buf = struct.unpack_from('Q3d4dII', data)
		ts = buf[0]
		translation = buf[1:4]
		rotation = buf[4:8]
		color_img_dim = buf[8:]
		color_img_size = color_img_dim[0]*color_img_dim[1]
		offset = 'Q3d4dII'
		color_image_vals = None
		if color_img_size > 0:
			offset_int = struct.calcsize(offset)
			color_image_vals = data[offset_int : offset_int + color_img_size*3]
			offset += '{0}B'.format(color_img_size*3)

		depth_image_dim = struct.unpack_from('II', data,struct.calcsize(offset))
		depth_image_size = depth_image_dim[0]*depth_image_dim[1]
		offset += 'II'
		depth_image_vals = None
		if depth_image_size > 0:
			#depth_image_vals = struct.unpack_from('{0}f'.format(depth_image_size), data, struct.calcsize(offset))
			depth_image_vals = data[offset_int : offset_int + struct.calcsize('{0}f'.format(depth_image_size))]
			offset += '{0}f'.format(depth_image_size)
		feelings = struct.unpack_from('4f', data, struct.calcsize(offset))

		color_image = (*color_img_dim, color_image_vals)
		depth_image = (*depth_image_dim, depth_image_vals)
		snapshot = Snapshot(ts, translation, rotation, color_image, depth_image, feelings)
		return snapshot
