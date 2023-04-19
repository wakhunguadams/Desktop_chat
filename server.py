import tkinter as tk
import socket
import threading

class Server:
    def __init__(self):
        self.host = "localhost"
        self.port = 5000

        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        self.clients = []
        self.nicknames = []

        self.server_window = tk.Tk()
        self.server_window.title("Server")

        self.log_label = tk.Label(self.server_window, text="Log:")
        self.log_label.pack()

        self.log_text = tk.Text(self.server_window)
        self.log_text.pack()

        self.send_message_label = tk.Label(self.server_window, text="Send message:")
        self.send_message_label.pack()

        self.send_message_entry = tk.Entry(self.server_window)
        self.send_message_entry.pack()

        self.send_message_button = tk.Button(self.server_window, text="Send", command=self.send_message)
        self.send_message_button.pack()

        self.server_window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.receive_thread = threading.Thread(target=self.receive_clients)
        self.receive_thread.start()

        self.server_window.mainloop()

    def receive_clients(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.log_text.insert(tk.END, f"Connected with {client_address}\n")
            client_socket.send("NICK".encode())
            nickname = client_socket.recv(1024).decode()
            self.nicknames.append(nickname)
            self.clients.append(client_socket)
            self.broadcast_message(f"{nickname} joined the chat!\n")
            client_socket.send("Connected to the server!\n".encode())
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                self.broadcast_message(message)
            except:
                index = self.clients.index(client_socket)
                self.clients.remove(client_socket)
                client_socket.close()
                nickname = self.nicknames[index]
                self.nicknames.remove(nickname)
                self.broadcast_message(f"{nickname} left the chat!\n")
                break

    def broadcast_message(self, message):
        self.log_text.insert(tk.END, message)
        for client in self.clients:
            client.send(message.encode())

    def send_message(self):
        message = self.send_message_entry.get()
        self.broadcast_message(f"Server: {message}\n")
        self.send_message_entry.delete(0, tk.END)

    def on_close(self):
        for client in self.clients:
            client.close()
        self.server_socket.close()
        self.server_window.destroy()

if __name__ == '__main__':
    Server()
