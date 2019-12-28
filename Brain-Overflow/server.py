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
from utils import parser
from utils import context

MAX_CLIENTS_NUMBER = 1000
HEADER_FORMAT = 'lli'
INCOMPLETE_MESSAGE_ERR = 'incomplete message'
TIME_RECORD_FORMAT = "%Y-%m-%d_%H-%M-%S-%f" #TODO - change format to *5* ms!

class Handler(threading.Thread):
    
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

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

        # generate the context for all parsers
        user_dir = self.data_dir + '/' + str(hello.user_id)
        p = Path(user_dir)
        self.lock.acquire()
        try:        
            #TODO - change to context
            if not p.exists():
                p.mkdir()
            datetime = dt.datetime.fromtimestamp(snapshot.timestamp/1000.0)
            print(datetime)
            datetime_in_format = datetime.strftime(TIME_RECORD_FORMAT)
            user_time_record_dir = Path(user_dir + '/' + \
                datetime_in_format )
            ## TODO chnage time record to required format
            if not user_time_record_dir.exists():
                user_time_record_dir.mkdir()

            #parse the supported fields
            con = context.Context(user_time_record_dir)
            for p in supported_parsers:
                print (p)
                supported_parsers[p](con, snapshot)

            #TODO - what about the case there are multiple snapshot is the same time??

        finally:
            self.lock.release()


@click.command()
@click.argument("address")
@click.argument("data_dir")
def run_server(address, data_dir):
    address_and_port = address.split(':')
    address_and_port[1] = int (address_and_port[1])
    address = tuple(address_and_port)

    server = Listener(address[1], address[0])
    server.start()

    while True:
        client = server.accept()
        handler = Handler(client, str(data_dir))
        handler.start()