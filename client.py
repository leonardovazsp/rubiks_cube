import cv2
import numpy as np
import os
import time
import requests
import random

post_url = "http://192.168.1.103:8000"

directory = r"C:\Users\leona\OneDrive\Documents\Python Projects\AI\rubiks_cube\train"

# os.chdir(directory)
def get_move(filename, move=''):
    
    r = requests.post(post_url, data=move)
    cube_pos = np.frombuffer(r.content).reshape(6,3,3,6)
    time.sleep(.25)
    cap = cv2.VideoCapture('http://192.168.1.103:8000/capture.mjpeg')
    ret, frame = cap.read()
    cv2.imwrite(filename + '.jpg', frame)
    np.save(filename + '.npy', cube_pos)    

for i in range(20):
    filename = os.path.join(directory, str(i))
    get_move(filename)

get_move('reset', move='reset')