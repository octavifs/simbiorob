#!/usr/bin/python

import os, sys
import time
import wiringpi
# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

class ServoSB(object):
  def __init__(self, pin):
    self.pin = int(pin)

class ServoWPI(object):
  def __init__(self, pin):
    self.pin = int(pin)
  
  def _hd_init(self):
    if self.pin == 18: # Use hardware PWM
      print("Initializing hardware PWM on pin #18")
      # set #18 to be a PWM output
      wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
      # set the PWM mode to milliseconds stype
      wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
      # divide down clock
      wiringpi.pwmSetClock(192)
      wiringpi.pwmSetRange(2000)
   
    else:
      print("Initializing hardware PWM on pin #%d"%self.pin)
      # set #pin to be a normal output
      wiringpi.pinMode(self.pin, wiringpi.GPIO.OUTPUT)
      # Setup software PWM using Pin, Initial Value and Range parameters
      wiringpi.softPwmCreate(self.pin, 0, 100)

  def pwm(self, pulse=100):
    if self.pin == 18:
      wiringpi.pwmWrite(self.pin, pulse)
    else:
      wiringpi.softPwmWrite(self.pin, pulse)

if __name__ == '__main__':
	s18 = ServoWPI(18)
	s18._hd_init()
	s18.test()
	while True: wiringpi.delay(100)
