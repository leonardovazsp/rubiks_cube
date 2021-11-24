import socketserver
import cube

cube = cube.Cube()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        move = str(self.data, 'utf-8')
        print(move)
        if move[-3:] == 'rev':
            cube.orientation = 0
            move = move[:-4]
        else:
            cube.orientation = 1
        print(move)
        move = getattr(cube, move)()
        move
        self.request.sendall(self.data.upper())

if __name__ == '__main__':
    HOST, PORT = '192.168.1.107', 9999

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()