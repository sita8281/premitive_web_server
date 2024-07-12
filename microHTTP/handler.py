import traceback
class Handler:
    def __init__(self):
        self._headers = {}
        self._method = ''
        self._http_ver = ''
        self._path = ''
        self._body = b''
        self._views = {}
        self._args = {}

    def set_views(self, views: dict):
        self._views = views

    def set_headers(self, headers: dict[str: str]) -> None:
        self._headers = headers

    def set_method(self, m: str):
        self._method = m

    def set_path(self, p: str):
        self._path = p

    def set_http_ver(self, v: str):
        self._http_ver = v

    def set_body(self, b: bytes):
        pass

    @property
    def get_len_body(self) -> int:
        len_body = self._headers.get('Content-Length')
        if len_body and len_body.isdigit():
            return int(len_body)
        return 0

    def handle(self):
        print(1)
        print(self._path)
        try:
            self._handle_path()
        except Exception as e:
            print(traceback.format_exc())
        func = self._views.get(self._path)

    def _handle_path(self):
        if '?' in self._path is False:
            return
        self._path, args = self._path.split('?', maxsplit=1)

        args = args.split('&')
        for arg in args:
            arg = arg.split('=')
            if len(arg) == 2:
                self._args[arg[0].strip()] = arg[1].strip()



