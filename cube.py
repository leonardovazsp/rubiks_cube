import time
import RPi.GPIO as GPIO
import numpy as np
import copy
import pickle
import inspect
import random

WAIT_TIME = 0.001

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pins = {'direction': 4,
        'top': 5,
        'bottom': 25,
        'front': 23,
        'back': 24,
        'right': 22,
        'left': 27}

for pin in pins.values():
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,False)

class Cube():
    def __init__(self):
        try:
            self.idx = np.load('cube_position.npy')
        except:
            self.idx = np.zeros((6,3,3))
            for i, face in enumerate(self.idx):
                face[:,:]=i
            np.save('cube_position.npy', self.idx)
        self.status = np.eye(6)[self.idx.astype(int)]
        self.orientation = 1
        self.history = self.get_history()
        self.moves = [self.right, self.right_rev, self.left, self.left_rev, self.top, self.top_rev, self.bottom, self.bottom_rev, self.front, self.front_rev, self.back, self.back_rev]
    
    def reset(self):
        for move in reversed(self.history):
            if move[-3:] == 'rev':
                move = move[:-4]
            else:
                move += '_rev'
            move = getattr(self, move)()
            move
        self.history = []
        self.save_history(self.history)

    def shuffle(self, n_iterations):
        for i in range(n_iterations):
            move = random.choice(self.moves)
            move()

    def random_move(self):
        move = random.choice(self.moves)
        move()
        return self.status

    def get_history(self):
        try:
            with open('moves_history', 'rb') as fp:
                my_list = pickle.load(fp)
        except:
            my_list = []
            with open('moves_history', 'wb') as fp:
                pickle.dump(my_list, fp)
        return my_list

    def save_history(self, my_list):
        with open('moves_history', 'wb') as fp:
            pickle.dump(my_list, fp)

    def move(self, pin, steps=50):
        for i in range(steps):
            GPIO.output(pin, True)
            time.sleep(WAIT_TIME)
            GPIO.output(pin, False)
            time.sleep(WAIT_TIME)
            
    def top(self):
        GPIO.output(pins['direction'], True)
        self.move(pins['top'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[0,0,:]=temp_idx[1,0,:]
        self.idx[1,0,:]=temp_idx[2,0,:]
        self.idx[2,0,:]=temp_idx[3,0,:]
        self.idx[3,0,:]=temp_idx[0,0,:]
        self.idx[4,:,:]=np.rot90(temp_idx[4,:,:],-1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)

    def top_rev(self):
        GPIO.output(pins['direction'], False)
        self.move(pins['top'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[0,0,:]=temp_idx[3,0,:]
        self.idx[1,0,:]=temp_idx[0,0,:]
        self.idx[2,0,:]=temp_idx[1,0,:]
        self.idx[3,0,:]=temp_idx[2,0,:]
        self.idx[4,:,:]=np.rot90(temp_idx[4,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)

    def right(self):
        GPIO.output(pins['direction'], True)
        self.move(pins['right'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[0,:,2]=temp_idx[5,:,2]
        self.idx[4,:,2]=temp_idx[0,:,2]
        self.idx[2,:,0]=np.flip(temp_idx[4,:,2],0)
        self.idx[5,:,2]=np.flip(temp_idx[2,:,0],0)
        self.idx[1,:,:]=np.rot90(temp_idx[1,:,:],-1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)

    def right_rev(self):
        GPIO.output(pins['direction'], False)
        self.move(pins['right'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[0,:,2]=temp_idx[4,:,2]
        self.idx[4,:,2]=np.flip(temp_idx[2,:,0],0)
        self.idx[2,:,0]=np.flip(temp_idx[5,:,2],0)
        self.idx[5,:,2]=temp_idx[0,:,2]
        self.idx[1,:,:]=np.rot90(temp_idx[1,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)
        
    def left(self):
        GPIO.output(pins['direction'], True)
        self.move(pins['left'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[0,:,0]=temp_idx[4,:,0]
        self.idx[4,:,0]=np.flip(temp_idx[2,:,2],0)
        self.idx[2,:,2]=np.flip(temp_idx[5,:,0],0)
        self.idx[5,:,0]=temp_idx[0,:,0]
        self.idx[3,:,:]=np.rot90(temp_idx[3,:,:],-1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)

    def left_rev(self):
        GPIO.output(pins['direction'], False)
        self.move(pins['left'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[0,:,0]=temp_idx[5,:,0]
        self.idx[4,:,0]=temp_idx[0,:,0]
        self.idx[2,:,2]=np.flip(temp_idx[4,:,0],0)
        self.idx[5,:,0]=np.flip(temp_idx[2,:,2],0)
        self.idx[3,:,:]=np.rot90(temp_idx[3,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)
        
    def bottom(self):
        GPIO.output(pins['direction'], True)
        self.move(pins['bottom'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[0,2,:]=temp_idx[3,2,:]
        self.idx[1,2,:]=temp_idx[0,2,:]
        self.idx[2,2,:]=temp_idx[1,2,:]
        self.idx[3,2,:]=temp_idx[2,2,:]
        self.idx[5,:,:]=np.rot90(temp_idx[5,:,:],-1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)

    def bottom_rev(self):
        GPIO.output(pins['direction'], False)
        self.move(pins['bottom'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[0,2,:]=temp_idx[1,2,:]
        self.idx[1,2,:]=temp_idx[2,2,:]
        self.idx[2,2,:]=temp_idx[3,2,:]
        self.idx[3,2,:]=temp_idx[0,2,:]
        self.idx[5,:,:]=np.rot90(temp_idx[5,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)

    def back(self):
        GPIO.output(pins['direction'], True)
        self.move(pins['back'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[1,:,2]=np.flip(temp_idx[5,2,:],0)
        self.idx[5,2,:]=temp_idx[3,:,0]
        self.idx[3,:,0]=np.flip(temp_idx[4,0,:],0)
        self.idx[4,0,:]=temp_idx[1,:,2]
        self.idx[2,:,:]=np.rot90(temp_idx[2,:,:],-1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)

    def back_rev(self):
        GPIO.output(pins['direction'], False)
        self.move(pins['back'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[1,:,2]=temp_idx[4,0,:]
        self.idx[5,2,:]=np.flip(temp_idx[1,:,2],0)
        self.idx[3,:,0]=temp_idx[5,2,:]
        self.idx[4,0,:]=np.flip(temp_idx[3,:,0],0)
        self.idx[2,:,:]=np.rot90(temp_idx[2,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)
    
    def front(self):
        GPIO.output(pins['direction'], True)
        self.move(pins['front'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[1,:,0]=temp_idx[4,2,:]
        self.idx[5,0,:]=np.flip(temp_idx[1,:,0],0)
        self.idx[3,:,2]=temp_idx[5,0,:]
        self.idx[4,2,:]=np.flip(temp_idx[3,:,2],0)
        self.idx[0,:,:]=np.rot90(temp_idx[0,:,:],-1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)

    def front_rev(self):
        GPIO.output(pins['direction'], False)
        self.move(pins['front'])
        temp_idx = copy.deepcopy(self.idx)
        self.idx[1,:,0]=np.flip(temp_idx[5,0,:],0)
        self.idx[5,0,:]=temp_idx[3,:,2]
        self.idx[3,:,2]=np.flip(temp_idx[4,2,:],0)
        self.idx[4,2,:]=temp_idx[1,:,0]
        self.idx[0,:,:]=np.rot90(temp_idx[0,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        self.history.append(inspect.currentframe().f_code.co_name)
        self.save_history(self.history)

if __name__ == '__main__':
    cube = Cube()
    cube.shuffle(14)

    time.sleep(1)
    cube.reset()