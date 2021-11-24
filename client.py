import socket
import sys

HOST, PORT = '192.168.1.107', 9999
data = " ".join(sys.argv[1:])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.sendall(bytes(data + '\n', 'utf-8'))

    received = str(sock.recv(1024), 'utf-8')

print(f"Sent: {data}")
print(f"Received: {received}")