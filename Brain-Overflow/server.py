import socket
import time
import datetime
from datetime import date
import threading
from pathlib import Path
import struct
from cli import CommandLineInterface
from thought import Thought
from utils import Connection
from utils import Listener

MAX_CLIENTS_NUMBER = 1000
HEADER_FORMAT = 'lli'
INCOMPLETE_MESSAGE_ERR = 'incomplete message'
TIME_RECORD_FORMAT = "%Y-%m-%d_%H-%M-%S"

class Handler(threading.Thread):
    
    lock = threading.Lock()

    def __init__(self, connection, data_dir):
        super().__init__()
        self.connection = connection
        self.data_dir = data_dir

    def run(self):
        header = self.connection.receive(struct.calcsize(HEADER_FORMAT))
        user_id, timestamp, thought_size = struct.unpack(HEADER_FORMAT, header)
        raw_thought = self.connection.receive(thought_size)
        thought = Thought.deserialize(header + raw_thought)
        self.connection.close()

        user_dir = self.data_dir + '/' + str(thought.user_id)
        p = Path(user_dir)
        self.lock.acquire()
        try:        
            if not p.exists():
                p.mkdir()
            user_time_record = Path(user_dir + '/' + \
                thought.timestamp.strftime(TIME_RECORD_FORMAT) +\
                 '.txt')

            thought_record = thought.thought
            if user_time_record.exists():
                thought_record = '\n' + thought_record

            with user_time_record.open(mode='a') as record:
                record.write(thought_record)

        finally:
            self.lock.release()

cli = CommandLineInterface()

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

@cli.command
def run(address, data):
    run_server(address, data)


def main(argv):
    cli.main()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))










    
