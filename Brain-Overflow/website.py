import functools
import http.server
import re

INVALID_HTTP_CODE_MSG = 'invalid http code'

def makeHandlerClass(handlers):
    class Handler(http.server.BaseHTTPRequestHandler):
        def send_headers(self, code, data_len=0):
            self.send_response(code)
            if code == 200:
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', data_len)
            elif code != 404:
                raise Exception(INVALID_HTTP_CODE_MSG)
            self.end_headers()


        def do_GET(self):
            for pattern in handlers:
                reg_ex = re.match('^' + pattern + '$', self.path)
                if reg_ex is not None:
                    arguments = reg_ex.groups()
                    code, body = handlers[pattern](*arguments)
                    self.send_headers(code, len(body))
                    self.wfile.write(body.encode())
                    return
            self.send_headers(404)
    return Handler

class Website:
    handlers = {}

    def route(self, path):
        def decorator(f):
            self.handlers[path] = f
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args,**kwargs)
            return wrapper
        return decorator

    def run(self, address):
        http_server = http.server.HTTPServer(address, makeHandlerClass(self.handlers))
        http_server.serve_forever()