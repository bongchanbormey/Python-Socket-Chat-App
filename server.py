import threading
import socket
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

def broadcast_message(message, addr=None):
    """Broadcast a message to all connected clients."""
    with clients_lock:
        for client in clients:
            try:
                if addr:  # If an address is provided, include it in the message
                    client.sendall(f"[{addr}] {message}".encode(FORMAT))
                else:  # Just send the message
                    client.sendall(message.encode(FORMAT))
            except:
                client.close()
                clients.remove(client)

def handle_client(conn, addr):
    """Handle communication with a single client."""
    print(f"[NEW CONNECTION] {addr} Connected")
    
    try:
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False
                continue

            # Timestamp each message
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{addr}] {msg} at {timestamp}")

            # Broadcast the message to all clients
            broadcast_message(f"{msg} at {timestamp}", addr)

    except ConnectionResetError:
        print(f"[ERROR] Connection with {addr} lost.")
    finally:
        with clients_lock:
            clients.remove(conn)
        conn.close()

def start():
    """Start the server and listen for incoming connections."""
    print('[SERVER STARTED]')
    server.listen()

    # Start a thread to handle incoming client connections
    threading.Thread(target=accept_connections, daemon=True).start()

    while True:
        # Input from server admin
        server_msg = input("Enter a message to send to all clients: ")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        broadcast_message(f"[Server] {server_msg} at {timestamp}")

def accept_connections():
    """Accept new client connections."""
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

start()
