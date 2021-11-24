import socketserver
import cube.py

cube = cube.Cube()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        move = 'cube.'+ str(self.data, 'utf-8')
        print(move)
        self.request.sendall(self.data.upper())

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()