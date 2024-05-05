from http_handler import HttpHandler
from socket_handler import SocketHandler
from pymongo import MongoClient


HTTP_PORT = 8000
SOCKET_PORT = 5000
MONGO_CLIENT = MongoClient('mongodb://mongo:567234@mongo:27017')

if __name__ == '__main__':
    HttpHandler.setup_ports(HTTP_PORT, SOCKET_PORT)
    http_thread = HttpHandler.start()

    socket_handler = SocketHandler(MONGO_CLIENT, SOCKET_PORT)
    socket_thread = socket_handler.start()
