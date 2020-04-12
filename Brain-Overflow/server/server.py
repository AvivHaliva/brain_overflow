import socket
import time
import threading
from thought import Thought
from utils import Connection
from utils import Listener
import click
from parsers import parser
from mq import MessageQueue
import struct
from utils.formats.client_server_communication import deserialize_client_message
from utils.formats.server_output_message import gen_server_output_message

from flask import Flask
from flask import request
import json

MAX_CLIENTS_NUMBER = 1000
HEADER_FORMAT = 'lli'
INCOMPLETE_MESSAGE_ERR = 'incomplete message'
TIME_RECORD_FORMAT = "%Y-%m-%d_%H-%M-%S-%f" #TODO - change format to *5* ms!

server = Flask(__name__)

@server.route('/config', methods=['GET'])
def handle_config_request():
    p = parser.Parser()
    supported_parsers = p.supported_parsers
    fields = []
    for par in supported_parsers:
        fields.append(supported_parsers[par].field)
    return json.dumps({'fields':fields})

def run_server_imp(host, port, to_publish):
    @server.route('/upload-snapshot', methods=['POST'])
    def handle_upload_snapshot_request():
        raw_message = request.get_data()
        user, snapshot = deserialize_client_message(raw_message)
        lock = threading.Lock()
        lock.acquire()
        try:
            output_message = gen_server_output_message(user, snapshot)
            to_publish(output_message)

        finally:
                lock.release()
        return '200'

    server.run(host=host, port=port, threaded=True, debug=True,)



@click.command()
@click.option('-h', '--host', default = '127.0.0.1', type=str)
@click.option('-p', '--port', default = 8000, type=int)
@click.argument('message_queue_url')
def run_server(host, port, message_queue_url):

    def publish_to_mq(message):
        p = parser.Parser()
        supported_parsers = p.supported_parsers

        mq = MessageQueue(message_queue_url)
        mq.declare_topic_exchange('snapshots_raw')

        for parser_name in supported_parsers:
            routing_key = parser_name + '.raw'
            mq.publish_to_queue('snapshots_raw', routing_key , message)
        #mq.close()
    
    run_server_imp(host, port, publish_to_mq)
