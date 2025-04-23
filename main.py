from http.server import HTTPServer
from app import database
from app.controllers.handler import Handler
from config import PORT


def run(server_class=HTTPServer, handler_class=Handler):
    database.initialize()
    server_address = ("", PORT)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == "__main__":
    run()
