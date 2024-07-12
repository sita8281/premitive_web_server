import socket
import time
import traceback


class Server(socket.socket):
    def __init__(self, class_handler, handler_args):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.setblocking(True)
        self._context_connect = None
        self._method = ''
        self._path = ''
        self._http_ver = ''
        self._headers = {}
        self._body_buffer = b''
        self._class_handler = class_handler
        self._handler_args = handler_args

    def _accept_connect(self):
        """Принятие нового TCP соединения"""
        while True:
            try:
                sock, addr = self.accept()
                self._context_connect = sock
                self._context_connect.settimeout(3)
                self._validate_headers()
            except socket.error:
                pass

    def _validate_headers(self):
        """Проверка заголовков HTTP"""
        buffer = b''
        while True:
            self._context_connect.settimeout(3)
            try:
                buffer += self._context_connect.recv(4096)
            except socket.timeout:
                self._context_connect.close()
                return
            if b'\r\n\r\n' in buffer:
                raw_headers, self._body_buffer = buffer.split(b'\r\n\r\n', maxsplit=1)
                self._parse_headers(raw_headers)
                handler = self._class_handler(views=self._handler_args)
                handler.set_headers(self._headers)
                handler.set_path(self._path)
                handler.set_http_ver(self._http_ver)
                handler.set_method(self._method)
                self._recv_body(handler.get_len_body)
                handler.set_body(self._body_buffer)
                handler.handle()
                self._context_connect.sendall(handler.get_response_raw())
                self._context_connect.close()

    def _recv_body(self, nbytes: int):
        while len(self._body_buffer) < nbytes:
            self._body_buffer += self._context_connect.recv()


    def _parse_headers(self, raw: bytes):
        ascii_headers = raw.decode('ascii').split('\r\n')

        self._method, self._path, self._http_ver = ascii_headers[0].split(' ')

        for row in ascii_headers[1:]:
            key, val = row.split(':', maxsplit=1)
            self._headers[key.strip()] = val.strip()


    def switching_to_handler(self):
        pass

    def run(self, host: str, port: int):
        """Запуск прослушки"""
        self.host = host
        self.port = port
        self.bind((self.host, self.port))
        self.listen(1)
        while True:
            try:
                self._accept_connect()
            except OSError:
                print('Ошибка сокета, перезапуск прослушки')
                time.sleep(1)
