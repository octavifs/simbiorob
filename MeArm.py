#!/usr/bin/python

import os, sys
import time
import wiringpi

class Servo(object):
  def __init__(self, pin):
    pass
  
  def hardware_init(self):
    # use 'GPIO naming'
    wiringpi.wiringPiSetupGpio()        
    # set #18 to be a PWM output
    wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

    # set the PWM mode to milliseconds stype
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

    # divide down clock
    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)

  def test(self):
    delay_period = 0.01

    while True:
      for pulse in range(50, 250, 1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)
      for pulse in range(250, 50, -1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)



if __name__ == '__main__':
	pass
