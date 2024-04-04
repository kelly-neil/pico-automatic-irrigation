from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse
import os
import json

web_path = os.path.join(os.path.abspath(__file__), 'web')

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)

        parsed = urlparse(self.path)
        abspath = os.path.join(web_path, parsed.path)

        if os.path.isdir(abspath):
            abspath = os.path.join(abspath, 'index.html')
        
        file_exists = os.path.isfile(abspath)
        
        if file_exists:
            file = open(abspath, 'r')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(file.read().encode())
            file.close()
        else:
            #non-file requests
            self.send_header('Content-type', 'text/json')
            if parsed.path == '/data/stats':
                self.wfile.write("Query received".encode())
         

httpd = HTTPServer(('localhost', 8000), Handler)
httpd.serve_forever()

# endpoint /data?
