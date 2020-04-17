import json
from ... import context
import struct
import datetime as dt
from ..client_server_communication import *

# fields naming #
USER_ID = 'user_id'
SNAPSHOT_ID = 'snapshot_id'
USERNAME = 'username'
BIRTHDAY = 'birthday'
GENDER = 'gender'
TIMESTAMP = 'timestamp'
POSE = 'pose'
TRANSLATION = 'translation'
ROTATION = 'rotation'
COLOR_IMAGE = 'color_image'
DEPTH_IMAGE = 'depth_image'
FEELINGS = 'feelings'
PARSER_NAME = 'parser_name'
USER_INFO = 'user_info'

# formats #
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
BIRTHDAY_FORMAT = "%Y-%m-%d"
COLOR_IMAGE_DIR = 'color_image'
DEPTH_IMAGE_DIR = 'depth_image'

# --------------- generating the format ---------------- #

def gen_server_output_message(user, snapshot):
    color_image_w, color_image_h, color_image_data = get_color_image_as_tuple(snapshot)
    depth_image_w, depth_image_h, depth_image_data = get_depth_image_as_tuple(snapshot)

    user_id = get_id(user)
    snapshot_id = get_datetime(snapshot)

    color_image_raw_path = save_bin_image(COLOR_IMAGE_DIR, color_image_data, user_id, snapshot_id)

    depth_image_data_bin = struct.pack(
        '{0}f'.format(depth_image_w * depth_image_h), *depth_image_data)
    depth_image_raw_path = save_bin_image(DEPTH_IMAGE_DIR, depth_image_data_bin, user_id, snapshot_id)

    user_info = {
        USERNAME : get_username(user),
        BIRTHDAY: get_birthday_as_str(get_birthday(user)),
        GENDER: get_gender(user),
    }

    return json.dumps({
    USER_ID: user_id,
    USER_INFO : user_info,
    SNAPSHOT_ID : snapshot_id,
    POSE : {
        TRANSLATION: get_translation_as_tuple(snapshot),
        ROTATION : get_rotation_as_tuple(snapshot)
        },
    TIMESTAMP: get_timestamp_as_str(get_datetime(snapshot) / 1000),
    COLOR_IMAGE: [color_image_w, color_image_h, color_image_raw_path],
    DEPTH_IMAGE: [depth_image_w, depth_image_h, depth_image_raw_path],
    FEELINGS: get_feelings_as_tuple(snapshot)})


def save_bin_image(image_type, image_data, user_id, snapshot_id):
    image_context = context.Context(user_id, snapshot_id, image_type)
    image_raw_path = image_context.save('raw', image_data, 'wb')
    return image_raw_path

def get_birthday_as_str(birthday_s):
	return covnvert_ms_to_datetime_str(birthday_s, BIRTHDAY_FORMAT)

def get_timestamp_as_str(datetime_ms):
	return covnvert_ms_to_datetime_str(datetime_ms, TIMESTAMP_FORMAT)

def covnvert_ms_to_datetime_str(ms, str_format):
	datetime_obj = dt.datetime.fromtimestamp(ms)
	return datetime_obj.strftime(str_format)

  	
# --------------- extracting values from format ---------------- #

def get_message_as_dict(message):
    #TODO - add try catch
    return json.loads(message)


