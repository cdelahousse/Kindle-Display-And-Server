#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from gen_image import gen_png_byte_stream
from config import PORT
import re

class KindleDisplayRequestHandler(BaseHTTPRequestHandler):
    def do_GET(client):
        path = client.path
        m = re.search(r'\d+$', path)

        if path == '/favicon.ico':
            client.send_response(404)
            client.end_headers()
        elif m != None and m.group(0).isdigit():
            client.send_response(200)
            client.send_header("Content-type", "image/png")
            client.end_headers()
            png_index = int(m.group(0))
            b = gen_png_byte_stream(png_index)
            client.wfile.write(b)

if __name__ == "__main__":
    print('Starting Kindle Display Image server on port %s' % PORT)
    srv = HTTPServer(('', PORT), KindleDisplayRequestHandler)
    srv.serve_forever()
