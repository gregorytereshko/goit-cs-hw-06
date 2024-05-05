from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import pathlib
import mimetypes
import socket
import threading


class HttpHandler(BaseHTTPRequestHandler):
    http_port = 8000
    socket_port = 5000

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        self.forward_data_to_socket(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def forward_data_to_socket(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(('localhost', 5000))
            sock.sendall(data)
            response = sock.recv(1024)
            print(f"Received from socket server: {response.decode()}")

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    @classmethod
    def setup_ports(cls, http_port, socket_port):
        cls.http_port = http_port
        cls.socket_port = socket_port

    @classmethod
    def start(cls):
        server_address = ('', cls.http_port)
        httpd = HTTPServer(server_address, cls)
        print(f"HTTP Server Running on port {cls.http_port}...")
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.start()
        return server_thread
