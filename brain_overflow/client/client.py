
from ..utils import Reader
from ..utils.formats.client_server_communication import gen_client_message

import requests
import json

GET_CONFIG_REQUEST = 'http://{0}:{1}/config'
UPLOAD_SNAPSHOT_REQUEST = 'http://{0}:{1}/upload-snapshot'

def upload_sample(path, host, port, file_format='protobuf'):
    reader = Reader(path, file_format)

    for snapshot in reader:
        user = reader.user
        response = requests.get(GET_CONFIG_REQUEST.format(host,port))
        fields = json.loads(response.content)['fields']

        requests.post(UPLOAD_SNAPSHOT_REQUEST.format(host,port),
        data = gen_client_message(user, snapshot, fields))
