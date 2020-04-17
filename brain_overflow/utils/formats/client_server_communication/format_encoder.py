from .user_pb2 import UserFormatted
from .snapshot_pb2 import SnapshotFormatted

import json
import struct
import io

# ******************** USER **************************** #

def gen_formatted_user(user_id, username, birthday, gender):
	user = UserFormatted()
	user.user_id = user_id
	user.username = username
	user.birthday = birthday
	#TODO handle gender
	if type(gender) != int:
		if gender == 'm':
			gender = 0
		elif gender == 'f':
			gender = 1
		else:
			gender = 2
	user.gender = gender
	return user

#TODO - add try catch in case non user message is supplied
def get_id(user_message):
	return user_message.user_id

def get_username(user_message):
	return user_message.username

def get_birthday(user_message):
	return user_message.birthday

def get_gender(user_message):
	return user_message.gender


# ******************** SNAPSHOT **************************** #

def gen_formatted_snapshot(datetime, translation_x, translation_y, translation_z,
		rotation_x, rotation_y, rotation_z, rotation_w, 
		color_image_w, color_image_h, color_image_data,
		depth_image_w, depth_image_h, depth_image_data_list, 
		feelings_hunger, feelings_thirst, feelings_exhaustion, feelings_happiness):
	snapshot = SnapshotFormatted()
	snapshot.datetime = datetime

	snapshot.pose.translation.x = translation_x
	snapshot.pose.translation.y = translation_y
	snapshot.pose.translation.z = translation_z

	snapshot.pose.rotation.x = rotation_x
	snapshot.pose.rotation.y = rotation_y
	snapshot.pose.rotation.z = rotation_z
	snapshot.pose.rotation.w = rotation_w

	snapshot.color_image.width = color_image_w
	snapshot.color_image.height = color_image_h
	snapshot.color_image.data = color_image_data

	snapshot.depth_image.width = depth_image_w
	snapshot.depth_image.height = depth_image_h
	snapshot.depth_image.data.extend(depth_image_data_list)

	snapshot.feelings.hunger = feelings_hunger
	snapshot.feelings.thirst = feelings_thirst
	snapshot.feelings.exhaustion = feelings_exhaustion
	snapshot.feelings.happiness = feelings_happiness

	return snapshot

def get_datetime(snapshot_message):
	return snapshot_message.datetime

def get_translation_as_tuple(snapshot_message):
	return (
		snapshot_message.pose.translation.x,
		snapshot_message.pose.translation.y,
		snapshot_message.pose.translation.z
		)

def get_rotation_as_tuple(snapshot_message):
	return (
		snapshot_message.pose.rotation.x,
		snapshot_message.pose.rotation.y,
		snapshot_message.pose.rotation.z,
		snapshot_message.pose.rotation.w
		)

def get_color_image_as_tuple(snapshot_message):
	return (
		snapshot_message.color_image.width,
		snapshot_message.color_image.height,
		snapshot_message.color_image.data
		)

def get_depth_image_as_tuple(snapshot_message):
	return (
		snapshot_message.depth_image.width,
		snapshot_message.depth_image.height,
		tuple(snapshot_message.depth_image.data)
		)

def get_feelings_as_tuple(snapshot_message):
	return (
		snapshot_message.feelings.hunger,
		snapshot_message.feelings.thirst,
		snapshot_message.feelings.exhaustion,
		snapshot_message.feelings.happiness
		)

# ******************** SERIALIZATION **************************** #

def serialize_message(message):
	return message.SerializeToString()

def gen_formatted_snapshot_required_only(client_snapshot, fields):
	fields.append('datetime')
	for field in [field.name for field in client_snapshot.DESCRIPTOR.fields]:
		if field not in fields:
			client_snapshot.ClearField(field)
	return client_snapshot


def gen_client_message(user, snapshot, fields):
	required_snapshot = gen_formatted_snapshot_required_only(snapshot, fields)
	serialized_user = serialize_message(user)
	serialized_snapshot = serialize_message(required_snapshot)
	user_len = struct.pack('I', len(serialized_user))
	snapshot_len = struct.pack('I', len(serialized_snapshot))
	return user_len + serialized_user + snapshot_len + serialized_snapshot

def deserialize_client_message(message):
	message = io.BytesIO(message)
	user_len, = struct.unpack('I', message.read(4))
	user =  deserialize_user_message(message.read(user_len))
	snapshot_len, = struct.unpack('I', message.read(4))
	snapshot =  deserialize_snapshot_message(message.read(snapshot_len))
	return user, snapshot

def deserialize_user_message(message):
	user = UserFormatted()
	user.ParseFromString(message)
	return user

def deserialize_snapshot_message(message):
	snapshot = SnapshotFormatted()
	snapshot.ParseFromString(message)
	return snapshot




