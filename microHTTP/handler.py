import io
import traceback
from .web_framework import Response, Request
from . import def_tmpl


class Handler:
    def __init__(self, views):
        self._headers = {}
        self._method = ''
        self._http_ver = ''
        self._path = ''
        self._data = b''
        self._body = b''
        self._views = views
        self._args = {}
        self._form = {}
        self._status = 200
        self._body_len = 0
        self._response_headers = {
            'Server': 'microHTTP',
            'Connection': 'close',
            'Content-Type': 'text/html; charset=utf-8',
            'Content-Length': f'{self._body_len}'
        }

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
        try:
            self._handle_path()
            view = self._views.get(self._path)
            if not view:
                self._status = 404
                self._body, self._body_len = def_tmpl.get_404
                return
            func, methods = view
            if not (self._method in methods):
                self._status = 405
                self._body, self._body_len = def_tmpl.get_405
                return
            response = func(Request(
                headers=self._headers,
                method=self._method,
                http_ver=self._http_ver,
                path=self._path,
                args=self._args,
                form=self._form,
                data=self._data
            ))

            self._headers.update(response.headers)
            self._body = response.body
            self._status = response.status
            self._body_len = response.body_len
        except Exception:
            self._status = 500
            self._body, self._body_len = def_tmpl.get_500
            self._body += b'\r\n' + str(traceback.format_exc()).encode('ascii')

    def _handle_path(self):
        if not ('?' in self._path):
            return
        self._path, args = self._path.split('?', maxsplit=1)

        args = args.split('&')
        for arg in args:
            arg = arg.split('=')
            if len(arg) == 2:
                self._args[arg[0].strip()] = arg[1].strip()

    def get_response_raw(self):
        buffer = f'{self._http_ver} {self._status}\r\n'
        if self._body_len > 0:
            self._response_headers['Content-Length'] = f'{self._body_len}'
        for key, val in self._response_headers.items():
            buffer += f'{key}: {val}\r\n'
        buffer += '\r\n'
        buffer = buffer.encode('ascii')
        if len(self._body) > 0:
            buffer += self._body
        return buffer

    def _handle_response(self, r):
        pass




