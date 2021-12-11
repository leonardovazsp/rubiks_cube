import time
import RPi.GPIO as GPIO
import numpy as np
import copy

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
        print('Loaded Cube: ', self.idx)
    
    def move(self, pin, steps=50):
        for i in range(steps):
            GPIO.output(pin, True)
            time.sleep(WAIT_TIME)
            GPIO.output(pin, False)
            time.sleep(WAIT_TIME)
            
    def top(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['top'])
        temp_idx = copy.deepcopy(self.idx)
        if self.orientation == 1:
            self.idx[0,0,:]=temp_idx[1,0,:]
            self.idx[1,0,:]=temp_idx[2,0,:]
            self.idx[2,0,:]=temp_idx[3,0,:]
            self.idx[3,0,:]=temp_idx[0,0,:]
            self.idx[4,:,:]=np.rot90(temp_idx[4,:,:],-1)
        else:
            self.idx[0,0,:]=temp_idx[3,0,:]
            self.idx[1,0,:]=temp_idx[0,0,:]
            self.idx[2,0,:]=temp_idx[1,0,:]
            self.idx[3,0,:]=temp_idx[2,0,:]
            self.idx[4,:,:]=np.rot90(temp_idx[4,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)

    def right(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['right'])
        temp_idx = copy.deepcopy(self.idx)
        if self.orientation == 1:
            self.idx[0,:,2]=temp_idx[5,:,2]
            self.idx[4,:,2]=temp_idx[0,:,2]
            self.idx[2,:,0]=np.flip(temp_idx[4,:,2],0)
            self.idx[5,:,2]=np.flip(temp_idx[2,:,0],0)
            self.idx[1,:,:]=np.rot90(temp_idx[1,:,:],-1)
        else:
            self.idx[0,:,2]=temp_idx[4,:,2]
            self.idx[4,:,2]=np.flip(temp_idx[2,:,0],0)
            self.idx[2,:,0]=np.flip(temp_idx[5,:,2],0)
            self.idx[5,:,2]=temp_idx[0,:,2]
            self.idx[1,:,:]=np.rot90(temp_idx[1,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        
    def left(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['left'])
        temp_idx = copy.deepcopy(self.idx)
        if self.orientation == 1:
            self.idx[0,:,0]=temp_idx[4,:,0]
            self.idx[4,:,0]=np.flip(temp_idx[2,:,2],0)
            self.idx[2,:,2]=np.flip(temp_idx[5,:,0],0)
            self.idx[5,:,0]=temp_idx[0,:,0]
            self.idx[3,:,:]=np.rot90(temp_idx[3,:,:],-1)
        else:
            self.idx[0,:,0]=temp_idx[5,:,0]
            self.idx[4,:,0]=temp_idx[0,:,0]
            self.idx[2,:,2]=np.flip(temp_idx[4,:,0],0)
            self.idx[5,:,0]=np.flip(temp_idx[2,:,2],0)
            self.idx[3,:,:]=np.rot90(temp_idx[3,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
        
    def bottom(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['bottom'])
        temp_idx = copy.deepcopy(self.idx)
        if self.orientation == 1:
            self.idx[0,2,:]=temp_idx[3,2,:]
            self.idx[1,2,:]=temp_idx[0,2,:]
            self.idx[2,2,:]=temp_idx[1,2,:]
            self.idx[3,2,:]=temp_idx[2,2,:]
            self.idx[5,:,:]=np.rot90(temp_idx[5,:,:],-1)
        else:
            self.idx[0,2,:]=temp_idx[1,2,:]
            self.idx[1,2,:]=temp_idx[2,2,:]
            self.idx[2,2,:]=temp_idx[3,2,:]
            self.idx[3,2,:]=temp_idx[0,2,:]
            self.idx[5,:,:]=np.rot90(temp_idx[5,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)

    def back(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['back'])
        temp_idx = copy.deepcopy(self.idx)
        if self.orientation == 1:
            self.idx[1,:,2]=np.flip(temp_idx[5,2,:],0)
            self.idx[5,2,:]=temp_idx[3,:,0]
            self.idx[3,:,0]=np.flip(temp_idx[4,0,:],0)
            self.idx[4,0,:]=temp_idx[1,:,2]
            self.idx[2,:,:]=np.rot90(temp_idx[2,:,:],-1)
        else:
            self.idx[1,:,2]=temp_idx[4,0,:]
            self.idx[5,2,:]=np.flip(temp_idx[1,:,2],0)
            self.idx[3,:,0]=temp_idx[5,2,:]
            self.idx[4,0,:]=np.flip(temp_idx[3,:,0],0)
            self.idx[2,:,:]=np.rot90(temp_idx[2,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)
    
    def front(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['front'])
        temp_idx = copy.deepcopy(self.idx)
        if self.orientation == 1:
            self.idx[1,:,0]=temp_idx[4,2,:]
            self.idx[5,0,:]=np.flip(temp_idx[1,:,0],0)
            self.idx[3,:,2]=temp_idx[5,0,:]
            self.idx[4,2,:]=np.flip(temp_idx[3,:,2],0)
            self.idx[0,:,:]=np.rot90(temp_idx[0,:,:],-1)
        else:
            self.idx[1,:,0]=np.flip(temp_idx[5,0,:],0)
            self.idx[5,0,:]=temp_idx[3,:,2]
            self.idx[3,:,2]=np.flip(temp_idx[4,2,:],0)
            self.idx[4,2,:]=temp_idx[1,:,0]
            self.idx[0,:,:]=np.rot90(temp_idx[0,:,:],1)
        self.status = np.eye(6)[self.idx.astype(int)]
        np.save('cube_position.npy', self.idx)

if __name__ == '__main__':
    cube = Cube()
    moves = [ cube.left, cube.top, cube.right, cube.back, cube.bottom, cube.front]
    for i in range(1):
        for move in moves:
            cube.orientation = 1
            move()
            cube.orientation = 0
            move()