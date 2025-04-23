from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from app.models.response import Response
from app.controllers.router import Router


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.router = Router()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed_url = urlparse(self.path)
        route_func, arg = self.router.match_path2route("GET", parsed_url.path)
        if not route_func:
            return Response(404, "404 Not Found").to_http(self)

        if parsed_url.query != "":
            response = route_func(parsed_url.query)
        else:
            response = route_func(arg) if arg else route_func()

        response.to_http(self)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        parsed_url = urlparse(self.path)
        route_func, arg = self.router.match_path2route("POST", parsed_url.path)
        if not route_func or arg:
            return Response(404, "404 Not Found").to_http(self)

        response = route_func(post_data.decode())

        response.to_http(self)

    def do_PATCH(self):
        content_length = int(self.headers["Content-Length"])
        patch_data = self.rfile.read(content_length)

        parsed_url = urlparse(self.path)
        route_func, codes = self.router.match_path2route("PATCH", parsed_url.path)
        if not route_func or not codes:
            return Response(404, "404 Not Found").to_http(self)

        response = route_func(patch_data.decode(), codes)

        response.to_http(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
