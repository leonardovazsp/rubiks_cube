from io import BytesIO
from time import sleep
from picamera import PiCamera
from flask import send_file
from flask import Flask
from flask import request
from cube import Cube
import numpy as np
from flask import jsonify

cube = Cube()

app = Flask(__name__)

@app.route('/get_image', methods = ['POST'])
def get_image():
    data = request.form
    move = data['move']
    move = getattr(cube, move)()
    move
    stream = BytesIO()
    with PiCamera() as camera:
        camera.start_preview()
        sleep(1)
        camera.capture(stream, format='jpeg')
    stream.seek(0)
    return send_file(stream, mimetype='image/jpeg')

@app.route('/random_move', methods = ['POST'])
def random_move():
    cube_position = cube.random_move()
    with PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 24
        sleep(1)
        output = np.empty((640, 480, 3), dtype='uint8')
        camera.capture(output, 'rgb')
    buf = BytesIO()
    np.savez_compressed(buf, output, cube_position)
    buf.seek(0)
    # print(buf)
    # print(type(np.load(buf)))
    # print(np.load(buf)['arr_0'])
    return send_file(buf, as_attachment=True, attachment_filename='a_file', mimetype='application/octet-stream')

app.run(debug=True, host='0.0.0.0')


