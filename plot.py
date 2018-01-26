#Based on code by Travis DeWolf - https://studywolf.wordpress.com/
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sympy as sp
from transforms3d._gohlketransforms import identity_matrix

np.set_printoptions(precision=3, suppress=True)  # neat printing

origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
I = identity_matrix()

class Sim(object):
  def __init__(self):
    self.time_elapsed = 0

  def reset(self, state):
    pass
    
  def step(self, state, u, dt):
    state[1] += u[0]
    state[2] += u[1]
    self.time_elapsed += dt

def getTv(vx,vy,vz):
  T = sp.Matrix(
    [[1, 0, 0, vx,],
     [0, 1, 0, vy],
     [0, 0, 1, vz],
     [0, 0, 0, 1]]
     )
  return T

def getRz(q):
  Tz = sp.Matrix(
    [[sp.cos(q), -sp.sin(q), 0, 0,],
     [sp.sin(q), sp.cos(q), 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]
     )
  return Tz
  
def getRx(q):
  Tx = sp.Matrix(
    [[1, 0, 0, 0],
     [sp.cos(q), -sp.sin(q), 0, 0,],
     [sp.sin(q), sp.cos(q), 0, 0],
     [0, 0, 0, 1]]
     )
  return Tx  

def getRy(q):
  Ty = sp.Matrix(
    [[sp.cos(q), 0, sp.sin(q), 0,],
     [0, 1, 0, 0],
     [-sp.sin(q), sp.cos(q), 0, 0],
     [0, 0, 0, 1]]
     )
  return Ty  



class Link(object):
  def __init__(self, i, l, axis, angle):
    self.i = i
    self.l = l # length of arm link in m
    self.axis = axis
    self.angle = angle
    
  def getHSym(self):
    R = None
    if self.axis == xaxis:
      R = getRx(sp.Symbol('q%d'%self.i))
    elif self.axis == yaxis:
      R = getRy(sp.Symbol('q%d'%self.i))
    elif self.axis == zaxis:
      R = getRz(sp.Symbol('q%d'%self.i))
    else:
      print "Error: unrecognized axis"            

    T = getTv(sp.Symbol('Vx%i'%self.i),sp.Symbol('Vy%i'%self.i),sp.Symbol('Vz%i'%self.i))
    return R*T
    
  def getH(self):
    H = self.getHSym()
    return np.matrix(H.subs(self.getSymbols()))

  def getSymbols(self):
    return {"q%d"%self.i:self.angle,
            "Vx%d"%self.i:self.l,
            "Vy%d"%self.i:0.0,
            "Vz%d"%self.i:0.0}

class BaseArm(object):
  def __init__(self):
    self.links = []
    self.init_state()
  
  def init_state(self):
    self.q = np.zeros(len(self.links)) # vector for current state    
    
  def add_link(self, v, axis=zaxis, angle=15):
    ran = math.radians(angle)
    self.links.append(Link(len(self.links),v, axis, ran))
    
  def compose(self):
    """Return direct kinematic transformation"""
    H = I.copy()
    for l in self.links:
      H *= l.getHSym()
      
    return H
    
  def subst(self, expr):
    d = {}
    for l in self.links:
      d.update(l.getSymbols())
    
    return np.matrix(expr.subs(d))
    
  def position(self):
    pass
    
  def plot(self):
    # set up figure and animation
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=(-1, 3), ylim=(-1, 3))
    ax.grid()
    
    O = np.matrix([0,0,0,1]).T
    lO = O
    for l in self.links:
      H = l.getH()
      #print "H:",H
      #print "lO:",lO
      nO = H*lO
      #print "nO:",nO
      line, = ax.plot([lO[0,0],nO[0,0]], [lO[1,0],nO[1,0]], 'o-', lw=4, mew=5)
      lO = nO    
  
if __name__ == "__main__":
  #arm = Test1LinkArm()
  #print "Original position:", arm.position()
  #target = np.asarray([1,1,1])
  
  #arm.move_to(target)
  arm = BaseArm()  
  arm.add_link(1.0,zaxis,25)
  arm.add_link(1.0,zaxis,45)
  arm.plot()
  
