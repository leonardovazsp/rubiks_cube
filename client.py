import cv2
import numpy as np
import os
import time
import requests
import random

class Generator():
    def __init__(self):
        self.post_url = "http://192.168.1.103:8000"
        self.directory = r"C:\Users\leona\OneDrive\Documents\Python Projects\AI\rubiks_cube\train2"
        self.moves_list = ['right', 'left', 'top', 'bottom', 'front', 'back']
        self.max_num = self.get_max_num()
        
    def get_max_num(self):
        filelist = os.listdir(self.directory)
        max_num = 0
        for file in filelist:
            if file[-3:] == 'npy' and file[:-4].isnumeric():
                num = int(file[:-4])
                if num > max_num:
                    max_num = num
        return max_num + 1
    
    def get_move(self, filename=None, move=None):
        if move is None:
            move  = random.choice(self.moves_list)
        r = requests.post(self.post_url, data=move)
        if filename is not None:
            filename = os.path.join(self.directory, filename)
            cube_pos = np.frombuffer(r.content).reshape(6,3,3,6)
            time.sleep(.25)
            cap1 = cv2.VideoCapture('http://192.168.1.103:8000/capture.mjpeg')
            cap2 = cv2.VideoCapture('http://192.168.1.117:8000/capture.mjpeg')
            ret, frame1 = cap1.read()
            ret, frame2 = cap2.read()
            cv2.imwrite(filename + '_1.jpg', frame1)
            cv2.imwrite(filename + '_2.jpg', frame2)
            np.save(filename + '.npy', cube_pos)

    def generate_examples(self, n_examples, reset=True):
        max_num = self.get_max_num()
        for i in range(max_num, max_num + n_examples):
            self.get_move(filename=str(i))
        if reset:
            self.get_move(filename='reset', move='reset')
            
            
if __name__ == '__main__':
    generator = Generator()
    # generator.generate_examples(2)
    for move in generator.moves_list:
        for i in range(4):
            generator.get_move(move=move)
            time.sleep(1)
    # generator.get_move(move='reset')

# # os.chdir(directory)
# def get_move(filename, move=''):
    
#     r = requests.post(post_url, data=move)
#     cube_pos = np.frombuffer(r.content).reshape(6,3,3,6)
#     time.sleep(.25)
#     cap1 = cv2.VideoCapture('http://192.168.1.103:8000/capture.mjpeg')
#     cap2 = cv2.VideoCapture('http://192.168.1.117:8000/capture.mjpeg')
#     ret, frame1 = cap1.read()
#     ret, frame2 = cap2.read()
#     cv2.imwrite(filename + '_1.jpg', frame1)
#     cv2.imwrite(filename + '_2.jpg', frame2)
#     np.save(filename + '.npy', cube_pos)    


# # for j in range(5):
# #     for i in range(2000, 2004):
# #         filename = os.path.join(directory, str(i))
# #         get_move(filename, move='top')
# #     for i in range(2000, 2004):
# #         filename = os.path.join(directory, str(i))
# #         get_move(filename, move='front')
# #     for i in range(2000, 2004):
# #         filename = os.path.join(directory, str(i))
# #         get_move(filename, move='left')
# #     for i in range(2000, 2004):
# #         filename = os.path.join(directory, str(i))
# #         get_move(filename, move='back')
# #     for i in range(2000, 2004):
# #         filename = os.path.join(directory, str(i))
# #         get_move(filename, move='bottom')
# #     for i in range(2000, 2004):
# #         filename = os.path.join(directory, str(i))
# #         get_move(filename, move='right')
# # for j in range(20):
# for i in range(max_num, max_num + 150):
#     filename = os.path.join(directory, str(i))
#     get_move(filename)
# filename = os.path.join(directory, 'reset')
# get_move(filename, move='reset')