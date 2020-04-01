import socket
import time
import datetime
import datetime as dt
import threading
from pathlib import Path
import struct
from thought import Thought
from utils import Connection
from utils import Listener
import click
from parsers import parser
from utils import context
from mq import MessageQueue
import json
import struct
from utils.formats.client_server_communication import *

MAX_CLIENTS_NUMBER = 1000
HEADER_FORMAT = 'lli'
INCOMPLETE_MESSAGE_ERR = 'incomplete message'
TIME_RECORD_FORMAT = "%Y-%m-%d_%H-%M-%S-%f" #TODO - change format to *5* ms!

def serialize_message(user, snapshot):
    color_image_w, color_image_h, color_image_data = get_color_image_as_tuple(snapshot)
    depth_image_w, depth_image_h, depth_image_data = get_depth_image_as_tuple(snapshot)
    
    color_image_context = context.Context(user.user_id, snapshot.datetime, 'color_image')
    color_image_raw_path = color_image_context.save('raw', color_image_data, 'wb')

    size = depth_image_w * depth_image_h
    depth_image_data_bin = struct.pack('{0}f'.format(size), *depth_image_data)

    depth_image_context = context.Context(user.user_id, snapshot.datetime, 'depth_image')
    depth_image_raw_path = depth_image_context.save('raw', depth_image_data_bin, 'wb')

    return json.dumps({
        'user_id': get_id(user),
        'user_name': get_username(user),
        'birthday': get_birthday(user),
        'gender': get_gender(user),
        'timestamp': get_datetime(snapshot),
        'translation': get_translation_as_tuple(snapshot),
        'rotation' : get_rotation_as_tuple(snapshot),
        'color_image': [color_image_w, color_image_h, color_image_raw_path],
        'depth_image': [depth_image_w, depth_image_h, depth_image_raw_path],
        'feelings': get_feelings_as_tuple(snapshot)})


class Handler(threading.Thread):
    
    lock = threading.Lock()

    def __init__(self, connection, to_publish):
        super().__init__()
        self.connection = connection
        self.to_publish = to_publish

    def run(self):
        #the server gets a user message from the client
        user_message = self.connection.receive_message()
        user = deserialize_user_message(user_message)
        
        #the server sends a config message to the client
        #TODO move parser initalization to the outside run / make singleton!
        p = parser.Parser()
        supported_parsers = p.supported_parsers
        #supported_parsers = parser.get_supported_functions()
        #config = protocol.Config(len(supported_parsers), list(supported_parsers.keys()))
        #self.connection.send_message(config.serialize())
        
        #the server gets a snapshot from the client
        snapshot_message = self.connection.receive_message()
        snapshot = deserialize_snapshot_message(snapshot_message)
        #close the connection
        self.connection.close()

        self.lock.acquire()
        try:
            serialized_message = serialize_message(user , snapshot)
            self.to_publish(serialized_message)

        finally:
            self.lock.release()


@click.command()
@click.option('-h', '--host', default = '127.0.0.1', type=str)
@click.option('-p', '--port', default = 8000, type=int)
@click.argument('message_queue_url')
def run_server(host, port, message_queue_url):

    server = Listener(int(port), host)
    server.start()

    def publish_to_mq(message):
        p = parser.Parser()
        supported_parsers = p.supported_parsers

        mq = MessageQueue(message_queue_url)
        mq.declare_topic_exchange('snapshots_raw')

        for parser_name in supported_parsers:
            routing_key = parser_name + '.raw'
            mq.publish_to_queue('snapshots_raw', routing_key , message)
        #mq.close()

    while True:
        client = server.accept()
        handler = Handler(client, publish_to_mq)
        handler.start()