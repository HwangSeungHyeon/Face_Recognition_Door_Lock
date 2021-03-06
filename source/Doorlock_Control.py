# 이 코드는 raspberry pi에서 사용하는 코드입니다.
# unlock() 코드를 실행하면 지정한 핀에 전류가 흐릅니다.
# lock() 코드를 실행하면 지정한 핀의 전류가 끊깁니다.

import RPi.GPIO as GPIO
import time

def test():
    unlock()
    lock()

def unlock(pin = 18):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.cleanup(pin)
    time.sleep(4)
    
def lock(pin = 18):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.cleanup(pin)
    time.sleep(1)
    
if __name__ == '__main__':
    unlock()
    lock()
    
    
