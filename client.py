import socket
import time
from datetime import datetime
import threading  # Make sure to import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

def receive_messages(connection):
    """Listen for incoming messages from the server."""
    while True:
        try:
            msg = connection.recv(1024).decode(FORMAT)
            if msg:
                print(msg)  # Display the message in the client terminal
        except Exception as e:
            print("Error receiving message:", e)
            break

def start():
    answer = input('Would you like to connect (yes/no)? ')
    if answer.lower() != 'yes':
        return

    connection = connect()
    
    # Start a thread to listen for incoming messages
    threading.Thread(target=receive_messages, args=(connection,), daemon=True).start()

    try:
        while True:
            msg = input("Message (q for quit): ")

            if msg == 'q':
                break

            # Include a timestamp when sending messages
            send(connection, f"{msg}")

    except (ConnectionResetError, BrokenPipeError):
        print("Connection lost.")
    finally:
        send(connection, DISCONNECT_MESSAGE)
        time.sleep(1)
        print('Disconnected')

start()
