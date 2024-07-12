from .handler import Handler
from .web_server import Server


class BaseHttpHandler(Handler):
    pass


class HttpServer:
    def __init__(self):
        self._routes = {}
        self._server = None

    def add_route(self, path: str, methods: list):
        def wrapper(func):
            self._routes[path] = func, methods
        return wrapper

    def run(self, host: str, port: int):
        self._server = Server(class_handler=BaseHttpHandler, handler_args=self._routes)
        self._server.run(host, port)





