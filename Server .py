import socket
import threading
import os
from ftplib import FTP
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# FTP server setup
def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", ".", perm="elradfmw")
    authorizer.add_anonymous(os.getcwd())

    handler = FTPHandler
    handler.authorizer = authorizer

    server = FTPServer(("127.0.0.1", 21), handler)
    server.serve_forever()

# Threaded client handler
def client_handler(conn, addr):
    print(f"New connection: {addr}")
    conn.send(b"Welcome to the Music Sharing App")

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received command: {data}")

            if data == "UPLOAD":
                filename = conn.recv(1024).decode()
                with open(filename, 'wb') as f:
                    while True:
                        bytes_read = conn.recv(1024)
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                conn.send(b"File uploaded successfully")

            elif data == "DOWNLOAD":
                filename = conn.recv(1024).decode()
                if os.path.exists(filename):
                    conn.send(b"READY")
                    with open(filename, 'rb') as f:
                        while True:
                            bytes_read = f.read(1024)
                            if not bytes_read:
                                break
                            conn.send(bytes_read)
                    conn.send(b"File downloaded successfully")
                else:
                    conn.send(b"File not found")
        
        except Exception as e:
            print(f"Error: {e}")
            break

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5000))
    server.listen(5)
    print("Server started, waiting for connections...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=client_handler, args=(conn, addr)).start()

if __name__ == "__main__":
    threading.Thread(target=start_ftp_server).start()
    start_server()
