import socketserver
import cube
import picamera
import io
from threading import Condition

cube = cube.Cube()

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

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
        # self.request.sendall(self.data.upper())
        try:
            while True:
                with output.condition:
                    output.condition.wait()
                    frame = output.frame
                self.request.sendall('frame')
        except Exception as e:
            logging.warning('Removed streaming client: %s', str(e))


if __name__ == '__main__':
    HOST, PORT = '192.168.1.107', 9999

    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        output = StreamingOutput()
        camera.rotation = 180
        camera.start_recording(output, format='mjpeg')

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()