import os
import platform
import requests
import sys
import stat
import socket
from subprocess import Popen

from . import config
from . import props


class CubrCore:
    def __init__(self, auth):
        self.auth = auth
        self.proc = None
        self.port = None
        self.URL = ""

    def start(self):
        if self.proc == None:
            exe_name = 'cubr'
            if platform.system() == 'Windows':
                exe_name += '.exe'
            core_path = os.path.join(os.path.dirname(__file__), exe_name)
            st = os.stat(core_path)
            os.chmod(core_path, st.st_mode | stat.S_IEXEC)

            sock = socket.socket()
            sock.bind(('', 0))
            self.port = str(sock.getsockname()[1])
            sock.close()
            self.URL = "http://localhost:" + self.port

            self.proc = Popen(
                [core_path, '-file-api-url', config.FILE_API_URL,
                    '-http-port', self.port],
                stdout=sys.stdout,
                stderr=sys.stderr,
            )

    def stop(self):
        if self.proc != None:
            self.proc.terminate()
            self.proc = None
            self.port = None

    def readline_callback(self, line):
        print(line)

    def emit_file_saved_event(self, file_path, file_id):
        return self.post("/events/file_saved", {'file_path': file_path, 'file_id': file_id})

    def get(self, path):
        return requests.get(self.URL + path, headers=self.auth.headers)

    def post(self, path, data):
        return requests.post(self.URL + path, json=data, headers=self.auth.headers)


def unregister():
    if props.props() != None:
        props.core().stop()
