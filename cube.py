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
        pass
    
    def move(self, pin, steps=50):
        for i in range(steps):
            GPIO.output(pin, True)
            time.sleep(WAIT_TIME)
            GPIO.output(pin, False)
            time.sleep(WAIT_TIME)
            
    def top(self, orientation=1):
        GPIO.output(pins['direction'], orientation)
        self.move(pins['top'])
        
    def right(self, orientation=1):
        GPIO.output(pins['direction'], orientation)
        self.move(pins['right'])
        
    def left(self, orientation=1):
        GPIO.output(pins['direction'], orientation)
        self.move(pins['left'])
        
    def bottom(self, orientation=1):
        GPIO.output(pins['direction'], orientation)
        self.move(pins['bottom'])
    
    def back(self, orientation=1):
        GPIO.output(pins['direction'], orientation)
        self.move(pins['back'])
    
    def front(self, orientation=1):
        GPIO.output(pins['direction'], orientation)
        self.move(pins['front'])

if __name__ == '__main__':
    cube = Cube()
    moves = [ cube.left, cube.top, cube.right, cube.back, cube.bottom, cube.front]
    for i in range(2):
        for move in moves:
            for i in range(4):
                move()