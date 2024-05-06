import socket
from multiprocessing import Process
import datetime


class SocketHandler:
    def __init__(self, mongo_client, port=5000):
        self.ip = 'localhost'
        self.port = port
        self.messages_table = mongo_client.hw06.messages

    def handle_client_connection(self, client_socket):
        try:
            while True:
                message = client_socket.recv(1024)
                if not message:
                    break
                print(f"Received message: {message.decode()}")
                message_data = dict(item.split('=')
                                    for item in message.decode().split('&'))
                message_data['date'] = datetime.datetime.now().isoformat()
                self.messages_table.insert_one(message_data)
                client_socket.sendall(b"Message received and stored")
        finally:
            client_socket.close()

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.ip, self.port))
        server_socket.listen(10)
        print(f"Socket server listening on {self.ip}:{self.port}")

        try:
            while True:
                client_sock, address = server_socket.accept()
                Process(target=self.handle_client_connection,
                        args=(client_sock,)).start()
        finally:
            server_socket.close()

    def start(self):
        process = Process(target=self.run)
        process.start()
        return process
