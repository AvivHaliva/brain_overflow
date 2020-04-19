
import socket
import time
import struct
from ..utils import Reader
from ..utils.formats.client_server_communication import gen_client_message

import requests
import json

def upload_sample(path, host, port, file_format):
    reader = Reader(path, file_format)

    for snapshot in reader:
        user = reader.user
        response = requests.get('http://{0}:{1}/config'.format(host,port))
        fields = json.loads(response.content)['fields']

        requests.post('http://{0}:{1}/upload-snapshot'.format(host,port),
        data = gen_client_message(user, snapshot, fields))
