#!/usr/bin/python

import os, sys

import transf as t
import sympy as sp
import numpy as np
import math
import matplotlib.pyplot as plt

def perpendicular(a) :
  b = np.empty_like(a)
  b[0] = -a[1]
  b[1] = a[0]
  return b
  
def normalize(a):
  a = np.array(a)
  return a/np.linalg.norm(a)  

def plot_refs(v0, v1):
  v = normalize(v1 - v0)
  p = perpendicular(v)
  xRef = np.concatenate((v0, v))
  yRef = np.concatenate((v0, p))
  return xRef, yRef

class Link(object):
  def __init__(self, i, l, axis, angle):
    self.i = i
    self.l = l # length of arm link in m
    self.axis = axis
    self.angle = angle
    
  def getHSym(self):
    R = None
    if self.axis == t.xaxis:
      R = t.getRx(sp.Symbol('q%d'%self.i))
    elif self.axis == t.yaxis:
      R = t.getRy(sp.Symbol('q%d'%self.i))
    elif self.axis == t.zaxis:
      R = t.getRz(sp.Symbol('q%d'%self.i))
    else:
      print "Error: unrecognized axis"            

    T = t.getTv(sp.Symbol('Vx%i'%self.i),sp.Symbol('Vy%i'%self.i),sp.Symbol('Vz%i'%self.i))
    return T*R
    
  def getH(self):
    H = self.getHSym()
    return sp.Matrix(H.subs(self.getSymbols()))

  def getSymbols(self):
    return {"q%d"%self.i:self.angle,
            "Vx%d"%self.i:self.l,
            "Vy%d"%self.i:0.0,
            "Vz%d"%self.i:0.0}


class MultiLink(object):
  def __init__(self):
    self.Torig = t.I.copy()
    self.links = []
    self.Hs = []
  
  def add_link(self, v, axis=t.zaxis, angle=15):
    ran = math.radians(angle)
    l = Link(len(self.links),v, axis, ran)
    self.links.append(l)

  def getLinkRef(self, ln, sym=False):
    "Return reference system for ln link"  

    H = self.Torig
    

  
  def compose(self, ln=None, sym=False):
    """Return direct kinematic transformation"""
    if not ln: ln = len(self.links)
    d = {}
    H = self.Torig
    for l in self.links[:ln]:
      print "Composing %d"%l.i
      d.update(l.getSymbols())
      H *= l.getHSym()
      sp.pprint(sp.Matrix(H.subs(d)))
    
    if not sym:
      return sp.Matrix(H.subs(d))
    else:
      return H
    
  def getLinks(self):
    return self.links

  def plot_links(self, fsize=(4,4), xl=(-2, 5),yl=(-2, 5)):
    # set up figure and animation
    fig = plt.figure(figsize=fsize)
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=xl, ylim=yl)
    ax.grid()
    
    O = sp.Matrix([0,0,0,1])
    lO = O

    H = t.I.copy()
    
    for l in links:
      H *= l.getH()
      print"O%d:"%l.i; sp.pprint(lO)
      print "H%d:"%l.i; sp.pprint(H)

      nO = sp.Matrix(H*lO)
      print "n%d:"%l.i,; sp.pprint(nO)

      # Calculate new reference system
      # Only for x and y, and casting to normal floats
      v0 = map(float,lO[:-2]); 
      v1 = map(float,nO[:-2]);
      
      #sp.pprint(v0)
      #sp.pprint(v1)
      
      ax.plot( (v0[0], v1[0]), (v0[1], v1[1]), 'o-', lw=4, mew=5, alpha=0.7)
      xRef, yRef = create_refs(np.asarray(v0), np.asarray(v1))
      ax.arrow(*xRef, head_width=0.05, head_length=0.1)
      ax.arrow(*yRef, head_width=0.05, head_length=0.1)

      lO = nO    

    return ax
    
if __name__ == '__main__':
  from sympy import init_printing, pprint
  init_printing() 

  sp.init_printing() 
  
  l = 1.0

  arm = MultiLink()  
  arm.add_link(l,t.zaxis,0)
  arm.add_link(l,t.zaxis,90)
  arm.add_link(l,t.zaxis,0)  
  
  #for l in arm.links:
  #  sp.pprint(l.getHSym())
  
  sp.pprint(arm.compose(sym=True))
  
  ax = arm.plot_links()

  lO = sp.Matrix([0,0,0,1])
  nO = sp.Matrix(arm.compose()*lO)
  v0 = map(float,lO[:-2]); 
  v1 = map(float,nO[:-2]);  

  sp.pprint(v0)
  sp.pprint(v1)  
  ax.plot( (v0[0], v1[0]), (v0[1], v1[1]),"k")
  
  plt.savefig("t1.png")

