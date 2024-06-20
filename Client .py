import socket
import os
import tkinter as tk
from tkinter import filedialog
from ftplib import FTP

class MusicSharingClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Sharing App")
        self.master.geometry("300x200")

        self.server_ip = "127.0.0.1"
        self.server_port = 5000

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.server_ip, self.server_port))

        self.label = tk.Label(master, text="Music Sharing App")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(master, text="Upload Music", command=self.upload_music)
        self.upload_button.pack(pady=5)

        self.download_button = tk.Button(master, text="Download Music", command=self.download_music)
        self.download_button.pack(pady=5)

        self.message_label = tk.Label(master, text="", fg="green")
        self.message_label.pack(pady=10)

    def upload_music(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.conn.send(b"UPLOAD")
            self.conn.send(os.path.basename(filename).encode())

            with open(filename, 'rb') as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    self.conn.send(bytes_read)

            self.message_label.config(text="File uploaded successfully")

    def download_music(self):
        filename = filedialog.asksaveasfilename(defaultextension=".mp3")
        if filename:
            self.conn.send(b"DOWNLOAD")
            self.conn.send(os.path.basename(filename).encode())

            data = self.conn.recv(1024)
            if data == b"READY":
                with open(filename, 'wb') as f:
                    while True:
                        bytes_read = self.conn.recv(1024)
                        if not bytes_read:
                            break
                        f.write(bytes_read)

                self.message_label.config(text="File downloaded successfully")
            else:
                self.message_label.config(text="File not found", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicSharingClient(root)
    root.mainloop()
