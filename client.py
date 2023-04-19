import socket
import threading
import tkinter as tk


class Client:
    def __init__(self):
        self.host = "localhost"  # or "127.0.0.1"
        self.port = 5000

        self.client_socket = socket.socket()
        self.client_socket.connect((self.host, self.port))

        self.client_window = tk.Tk()
        self.client_window.title("Client")

        self.log_label = tk.Label(self.client_window, text="Log:")
        self.log_label.pack()

        self.log_text = tk.Text(self.client_window)
        self.log_text.pack()

        self.message_label = tk.Label(self.client_window, text="Message:")
        self.message_label.pack()

        self.message_entry = tk.Entry(self.client_window)
        self.message_entry.pack()

        self.send_button = tk.Button(self.client_window, text="Send", command=self.send_message)
        self.send_button.pack()

        self.client_window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        self.client_window.mainloop()

    def send_message(self):
        message = self.message_entry.get()
        self.client_socket.send(message.encode())
        self.message_entry.delete(0, tk.END)

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                self.log_text.insert(tk.END, data + "\n")

            except ConnectionResetError:
                self.log_text.insert(tk.END, "Server disconnected\n")
                self.client_socket.close()
                break

    def on_close(self):
        self.client_socket.close()
        self.client_window.destroy()


if __name__ == '__main__':
    Client()
