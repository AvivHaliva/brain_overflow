import struct

HELLO_MESSAGE_FORMAT = 'QI{0}sIc'
SNAPSHOT_MESSAGE_FORMAT = 'Q3d4dII{0}*3bII{1}f4f'

class Hello_Message:
	def __init__(self, user_id, user_name, user_birth_date, user_gender):
		self.user_id = user_id
		self.user_name = user_name
		self.user_birth_date = user_birth_date
		self.user_gender = user_gender

	def serialize(self):
		serialized_hello_message = struct.pack(HELLO_MESSAGE_FORMAT,\
			self.user_id, \
			len(self.user_name.encode()), \
			self.user name.encode(), \
			self.user_birth_date,\
			self.user_gender)
		return serialized_hello_message

	def deserialize(data):
		user_id, _, user_name_bin, birth_date, gender = \
		 struct.unpack(HELLO_MESSAGE_FORMAT, data)
		user_name = user_name_bin.decode()
		return Hello_Message(user_id, user_name, birth_date, gender)

class Config_Message:
	def __init__(self, fields_num, fields):
		self.fields_num = fields_num
		self.fields = fields

	def serialize(self):
		serialized_config_message = 
		encoded_fields = [f.encode() for f in self.fields]
		encoded_fields_len = [len(f) for f in encoded_fields]
		config_format = 'I'
		data = [self.fields_num]
		for i in range(encoded_fields_len):
			config_format += 'I{0}s'.format(encoded_fields_len[i])
			data.append(encoded_fields_len[i])
			data.append(encoded_fields[i])

		data = tuple(data)
		serialized_config_message = struct.pack(config_format, *data)
		return serialized_config_message

	def deserialize(data):
		fields_num = data.unpack('I', data)
		fields = []
		offset = struct.calcsize('I')
		for i in range(fields_num):
			curr_field_size = data.unpack('I', data)
			offset += struct.calcsize('I')
			curr_field = data.unpack('{0}s'.format(curr_field_size),\
				data, offset).decode()
			fields.append(curr_field)
			offset += curr_field_size

		fields = tuple(fields)
		Config_message = Config_Message(fields_num, *fields)


class Snapshot_Message:
	def __init__(self, \
		ts, \
		transalation, \
		 rotation, \
		  color_image=(0,0,None),\
		   depth_image=(0,0,None),\
		   user_feelings=(0,0,0,0)
		   ):
		self.timestamp = ts
		self.transalation = transalation
		self.rotation = rotation
		self.color_image = color_image
		self.depth_image = depth_image
		self.user_feelings = user_feelings


	def serialized(self):
		color_img_size = self.color_image[0]*self.color_image[1]
		depth_img_size = self.depth_image[0]*self.depth_image[1]
		serialized_snapshot = struct.pack\
		(SNAPSHOT_MESSAGE_FORMAT.format(color_img_size, depth_img_size),\
			self.timestamp, *self.transalation, *self.rotation, *self.color_image,\
			*self.depth_image, *self.user_feelings)
		return serialized_snapshot

	def deserialized(data):
		ts, (tx, ty, tz), (rx, ry, rz, rw), (ci_h, ci_w) = 
			struct.unpack('Q3d4dII', data)
		color_img_size = ci_h*ci_w
		color_image_vals, di_h, di_w = struct.unpack('{0}*3bII'.format(color_img_size), data,struct.calcsize('Q3d4dII'))
		depth_image_size = di_h*di_w
		depth_image_vals, (hunger, thirst, exhaustion, happinness) = \
		struct.unpack('{0}f4f'.format(depth_img_size), data, struct.calcsize('Q3d4dII'+'{0}*3bII'.format(color_img_size)))

		snapshot = Snapshot_Message(ts, (tx,ty,tz), (rx, ry, rz, rw),\
			(ci_h, ci_w, color_image_vals), (di_h, di_w,depth_image_vals),\
			(hunger,thirst.exhaustion,happinness))
		return snapshot

