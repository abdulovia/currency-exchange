import json


class Response:
    def __init__(self, code: int, message: str, body: dict=None):
        self.code = code
        self.message = message
        self.body = body

    def to_http(self, handler):
        message_dct = {"message": self.message}
        handler.send_response(self.code, message_dct)

        handler.send_header("Access-Control-Allow-Origin", "*")
        handler.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        handler.send_header("Access-Control-Allow-Headers", "Content-Type")

        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(
            json.dumps(self.body).encode()
            if self.body
            else json.dumps(message_dct).encode()
        )
