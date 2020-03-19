import socket
import time
import struct
from thought import Thought
from utils import Connection
import click
from utils import Reader
from utils import protocol

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

@click.command()
@click.argument('path')
@click.argument('address')
@click.argument('file_format')
def upload_sample(path, address, file_format):
    #TODO 
    reader = Reader(path, file_format)
    address_and_port = address.split(':')
    address_and_port[1] = int(address_and_port[1])
    address_and_port = tuple(address_and_port)
    i = 0
    for snapshot in reader:
        print(i)
        i = i + 1
        with Connection.connect(*address_and_port) as connection:
            user = reader.user
            hello_message = protocol.Hello(user.id, user.name, user.birth_date, user.gender)
            connection.send_message(hello_message.serialize())
            config_message = connection.receive_message()
            config = protocol.Config.deserialize(config_message)
            snapshot_message = protocol.Snapshot(snapshot.timestamp)
            for field in config.fields:
                setattr(snapshot_message,field, snapshot.__dict__[field])
            connection.send_message(snapshot_message.serialize())