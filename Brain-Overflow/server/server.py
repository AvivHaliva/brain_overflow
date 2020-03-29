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
from utils import protocol
from parsers import parser
from utils import context
from mq import MessageQueue
import json

MAX_CLIENTS_NUMBER = 1000
HEADER_FORMAT = 'lli'
INCOMPLETE_MESSAGE_ERR = 'incomplete message'
TIME_RECORD_FORMAT = "%Y-%m-%d_%H-%M-%S-%f" #TODO - change format to *5* ms!

def serialize_message(user, snapshot):
    color_image_w, color_image_h, color_image_data = snapshot.color_image
    depth_image_w, depth_image_h, depth_image_data = snapshot.depth_image
    return json.dumps({
        'user_id': user.user_id,
        'user_name': user.user_name,
        'birthday': user.user_birth_date,
        'gender': user.user_gender,
        'timestamp': snapshot.timestamp,
        'translation': snapshot.translation,
        'rotation': snapshot.rotation,
        'color_image': [color_image_w, color_image_h, color_image_data],
        'depth_image': [depth_image_w, depth_image_h, depth_image_data],
        'feelings': snapshot.feelings})


class Handler(threading.Thread):
    
    lock = threading.Lock()

    def __init__(self, connection, to_publish):
        super().__init__()
        self.connection = connection
        self.to_publish = to_publish

    def run(self):
        #the server gets a hello message from the client
        hello_message = self.connection.receive_message()
        hello = protocol.Hello.deserialize(hello_message)
        
        #the server sends a config message to the client
        #TODO move parser initalization to the outside run / make singleton!
        p = parser.Parser()
        supported_parsers = p.supported_parsers
        #supported_parsers = parser.get_supported_functions()
        config = protocol.Config(len(supported_parsers), list(supported_parsers.keys()))
        self.connection.send_message(config.serialize())
        
        #the server gets a snapshot from the client
        snapshot_message = self.connection.receive_message()
        snapshot = protocol.Snapshot.deserialize(snapshot_message)
        #close the connection
        self.connection.close()

        self.lock.acquire()
        try:
            serialized_message = serialize_message(hello , snapshot)
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
        mq = MessageQueue(message_queue_url)
        mq.declare_broadcast_queue('snapshots_raw')
        mq.publish_to_queue('snapshots_raw', '', message)
        #mq.close()

    while True:
        client = server.accept()
        handler = Handler(client, publish_to_mq)
        handler.start()