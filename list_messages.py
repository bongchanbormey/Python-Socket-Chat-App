import socket
import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

def receive_messages(client):
    """Function to continuously receive messages from the server."""
    while True:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg:
                print(msg)
        except ConnectionResetError:
            print("Connection lost.")
            break

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def start():
    client = connect()
    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        pass  # The client only receives messages in this version.

start()
