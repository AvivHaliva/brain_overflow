from pathlib import Path
import datetime
from flask import Flask
import click

app = Flask(__name__)
DATA_DIR_PATH = '/'

FILE_TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
WEB_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

_INDEX_HTML = '''
<html>
    <head>Brain Computer Interface</head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''

_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''

_USER_PAGE_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>
'''

_THOUGHT_LINE_HTML = '''
<tr>
    <td>{thought_time}</td>
    <td>{thought}</td>
</tr>
'''

def get_users_list():
    users_list = []
    for user_dir in Path(DATA_DIR_PATH).iterdir():
        users_list.append(user_dir.name)
    return users_list

@app.route('/')
def get_users_page():
    users_html = []
    for user_dir in get_users_list():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return index_html , 200

@app.route('/users/<int:user_id>')
def get_user_thoughts(user_id):
    user_id = str(user_id)
    if user_id not in get_users_list():
        return '', 404
    thoughts_list_html = []
    for file in Path(DATA_DIR_PATH + '/' + user_id).iterdir():
        f = file.open('r')
        for thought in f.readlines():
            thought_time = file.name[:-4]
            thought_time = datetime.datetime.strptime(thought_time, FILE_TIME_FORMAT)
            thought_time = thought_time.strftime(WEB_TIME_FORMAT)
            thoughts_list_html.append(_THOUGHT_LINE_HTML.format(thought_time=thought_time, thought=thought))
    user_thought_html = \
        _USER_PAGE_HTML.format(user_id=user_id, thoughts='\n'.join(thoughts_list_html))    
    return user_thought_html, 200

@click.command()
@click.argument('address')
@click.argument('data_dir')
def run_webserver(address, data_dir):
    global DATA_DIR_PATH
    DATA_DIR_PATH = data_dir
    address_and_port = address.split(':')
    port = int (address_and_port[1])
    host = address_and_port[0]
    #TODO - remove debug
    app.run(host=host, port=port, debug=True)

'''
    except Exception as error:
        print(f'ERROR: {error}')
        return 1
'''