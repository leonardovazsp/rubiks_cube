import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handler(self):
        self.data = self.request.recv(1024).strip()
        print(f"{self.client_address} wrote:")
        print(self.data)
        self.request.sendall(self.data.upper())

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()