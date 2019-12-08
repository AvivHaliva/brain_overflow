import socket
import time
import struct
from thought import Thought
from utils import Connection
import click

@click.command()
@click.argument('address')
@click.argument('user_id')
@click.argument('thought')
def upload_thought(address, user_id, thought):
    address_and_port = address.split(':')
    address_and_port[1] = int(address_and_port[1])
    address_and_port = tuple(address_and_port)

    conn = socket.socket()
    conn.connect(address_and_port)
    connection = Connection(conn)

    thought = Thought(int(user_id),  int(time.time()), thought)
    serialized_thought = Thought.serialize(thought)
    connection.send(serialized_thought)
    print('done')
    connection.close()