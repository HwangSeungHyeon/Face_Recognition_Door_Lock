# 이 코드는 raspberry pi에서 사용하는 코드입니다.
# only raspberri pi

import RPi.GPIO as GPIO
import time

def unlock(pin=18):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    
def lock(pin=18):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
if __name__ == '__main__':
    unlock()
    time.sleep(2)
    lock()
    GPIO.cleanup(18)
