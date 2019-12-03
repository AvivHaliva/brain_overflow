import http.server
from pathlib import Path
import datetime
import os
from website import Website

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

website = Website()

def get_users_list():
    users_list = []
    for user_dir in Path(os.getcwd()).iterdir():
        users_list.append(user_dir.name)
    return users_list

@website.route('/')
def get_users_page():
    users_html = []
    for user_dir in get_users_list():
        users_html.append(_USER_LINE_HTML.format(user_id=user_dir))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    return 200, index_html

@website.route('/users/([0-9]+)')
def get_user_thoughts(user_id):
    if user_id not in get_users_list():
        return 404, ''
    thoughts_list_html = []
    for file in Path(os.getcwd() + '/' + user_id).iterdir():
        f = file.open('r')
        for thought in f.readlines():
            thought_time = file.name[:-4]
            thought_time = datetime.datetime.strptime(thought_time, FILE_TIME_FORMAT)
            thought_time = thought_time.strftime(WEB_TIME_FORMAT)
            thoughts_list_html.append(_THOUGHT_LINE_HTML.format(thought_time = thought_time, thought = thought))
    user_thought_html = _USER_PAGE_HTML.format(user_id = user_id, thoughts = '\n'.join(thoughts_list_html))    
    return 200, user_thought_html

def run_webserver(address, data_dir):
    os.chdir(data_dir)
    website.run(address)

def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        address_and_port = argv[1].split(':')
        address_and_port[1] = int (address_and_port[1])
        address_and_port = tuple(address_and_port)
        run_webserver(address_and_port, argv[2])
    except Exception as error:
        print(f'ERROR: {error}')
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))