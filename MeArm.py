#!/usr/bin/python

import os, sys
import time
import wiringpi
import pythonSB as sb
# use 'GPIO naming'
#wiringpi.wiringPiSetupGpio()

class ServoSB(object):
  def __init__(self, pin, minAngle=5, maxAngle=175):
    """Pin number, min us output, max us output, min angle, max angle """ 
    self.pin = int(pin)
    self.minUS = 1000
    self.maxUS = 2000
    self.minAngle = minAngle
    self.maxAngle = maxAngle
    self._configure()

  def _configure(self):
    sb.servo_configure(self.pin, 
          self.minUS, self.maxUS, self.minAngle, self.maxAngle) 

  def set_angle(self, angle):
    sb.servo_set_angle(self.pin, int(angle))

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
  s7 = Servo(7)
  s7.set_angle(90)
