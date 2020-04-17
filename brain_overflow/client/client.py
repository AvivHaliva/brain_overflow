
import socket
import time
import struct
import click
from ..utils import Reader
from ..utils.formats.client_server_communication import gen_client_message

import requests
import json

@click.command()
@click.argument('path')
@click.argument('address')
@click.argument('file_format')
def upload_sample(path, address, file_format):
    reader = Reader(path, file_format)
    address_and_port = address.split(':')
    address_and_port[1] = int(address_and_port[1])
    address_and_port = tuple(address_and_port)

    host = address_and_port[0]
    port = address_and_port[1]

    for snapshot in reader:
        user = reader.user
        response = requests.get('http://{0}:{1}/config'.format(host,port))
        fields = json.loads(response.content)['fields']

        requests.post('http://{0}:{1}/upload-snapshot'.format(host,port),
        data = gen_client_message(user, snapshot, fields))
