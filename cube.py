import time
import RPi.GPIO as GPIO

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
        self.orientation = 1
    
    def move(self, pin, steps=50):
        for i in range(steps):
            GPIO.output(pin, True)
            time.sleep(WAIT_TIME)
            GPIO.output(pin, False)
            time.sleep(WAIT_TIME)
            
    def top(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['top'])
        
    def right(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['right'])
        
    def left(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['left'])
        
    def bottom(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['bottom'])
    
    def back(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['back'])
    
    def front(self):
        GPIO.output(pins['direction'], self.orientation)
        self.move(pins['front'])

if __name__ == '__main__':
    cube = Cube()
    moves = [ cube.left, cube.top, cube.right, cube.back, cube.bottom, cube.front]
    for i in range(1):
        for move in moves:
            for i in range(4):
                move()