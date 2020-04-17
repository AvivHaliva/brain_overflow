from .. import server_output_message as mq_snapshot_output_encoder
import json

# fields naming #
USER_ID = 'user_id'
SNAPSHOT_ID = 'snapshot_id'
TIMESTAMP = 'timestamp'
PARSER_NAME = 'parser_name'
USER_INFO = 'user_info'


def gen_parser_input_message(snapshot_message):
	snapshot = mq_snapshot_output_encoder.get_message_as_dict(snapshot_message)
	return snapshot

def gen_parser_output_message(snapshot_dict, parser_name, parser_res):
	user_id = snapshot_dict[mq_snapshot_output_encoder.USER_ID]
	timestamp = snapshot_dict[mq_snapshot_output_encoder.TIMESTAMP]
	snapshot_id = snapshot_dict[SNAPSHOT_ID]
	user_info = snapshot_dict[USER_INFO]

	message = {
		USER_ID: user_id,
		USER_INFO : user_info,
		TIMESTAMP : timestamp,
		SNAPSHOT_ID : snapshot_id,
		PARSER_NAME : parser_name,
		parser_name : parser_res
	}

	return json.dumps(message)





