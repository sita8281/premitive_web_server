import os.path


class Response:
    def __init__(self, status: int, headers: dict = None, body: bytes = b'', template: str = ''):
        self.status = status
        self.headers = headers
        self.body = body
        self.template_path = template
        self.body_len = 0

        if not headers:
            self.headers = {}

        if self.template_path:
            self.body = self.html()

    def html(self):
        normalize_path = os.path.join(os.path.dirname(__file__), f'../templates/{self.template_path}')
        with open(file=normalize_path, mode='rb') as file:
            data = file.read()
            self.body_len = len(data)
            return data


class Request:
    def __init__(self, headers, method, http_ver, path, args, form, data):
        self.headers: dict[str: str] = headers
        self.method: str = method
        self.http_ver: str = http_ver
        self.path: str = path
        self.args: dict[str: str] = args
        self.form: dict[str: str] = form
        self.data: bytes = data





