import socket
import time
import struct
from cli import CommandLineInterface
from thought import Thought
from utils import Connection

cli = CommandLineInterface()

def upload_thought(address, user_id, thought):
    conn = socket.socket()
    conn.connect(address)
    connection = Connection(conn)

    thought = Thought(user_id,  int(time.time()), thought)
    serialized_thought = Thought.serialize(thought)
    connection.send(serialized_thought)
    print('done')
    connection.close()

@cli.command
def upload(address, user, thought):
    address_and_port = address.split(':')
    address_and_port[1] = int(address_and_port[1])
    address_and_port = tuple(address_and_port)
    upload_thought(address_and_port, int(user),thought)

def main(argv):
    cli.main()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
