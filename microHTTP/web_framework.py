

class DefaultResponse:
    def __init__(self):

class Response:
    def __init__(self, status: int, headers: dict, body: bytes):
        pass


class Request:
    def __init__(self, headers, method, http_ver, path, args):
        self.headers = {}
        self.method = ''
        self.http_ver = ''
        self.path = ''
        self.args = {}


