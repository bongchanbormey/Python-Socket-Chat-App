import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Application")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.text_area.pack(pady=10)
        self.text_area.config(state='disabled')

        self.msg_entry = tk.Entry(self.root, width=50)
        self.msg_entry.pack(pady=5)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()


    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode(FORMAT)
                if msg:
                    self.text_area.config(state='normal')
                    self.text_area.insert(tk.END, msg + '\n')
                    self.text_area.config(state='disabled')
                    self.text_area.yview(tk.END)
            except ConnectionResetError:
                break


    def send_message(self):
        msg = self.msg_entry.get()
        if msg:
            self.client.sendall(f" {msg}".encode(FORMAT))
            self.msg_entry.delete(0, tk.END)


def start_client():
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()

start_client()
