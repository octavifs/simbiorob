import math
import sys
import numpy as np
import sympy as sp

from anytree import Node, RenderTree, PreOrderIter

import matplotlib.pyplot as plt
from IPython.display import display
from cycler import cycler
import matplotlib.colors as colors
import matplotlib.cm as cmx

#### Basic defitions
xaxis = sp.Matrix([1,0,0,1]).T
yaxis = sp.Matrix([0,1,0,1]).T
zaxis = sp.Matrix([0,0,1,1]).T

#### Basic functions
def identity():
  T = sp.Matrix(
    [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]
     )
  return T

def transl(vx,vy,vz):
  T = sp.Matrix(
    [[1, 0, 0, vx],
     [0, 1, 0, vy],
     [0, 0, 1, vz],
     [0, 0, 0, 1]]
     )
  return T

def rotz(q):
  Tz = sp.Matrix(
    [[sp.cos(math.radians(q)), -sp.sin(math.radians(q)), 0, 0],
     [sp.sin(math.radians(q)), sp.cos(math.radians(q)), 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]
     )
  return Tz
  
def rotx(q):
  Tx = sp.Matrix(
    [[1, 0, 0, 0],
     [sp.cos(math.radians(q)), -sp.sin(math.radians(q)), 0, 0],
     [sp.sin(math.radians(q)), sp.cos(math.radians(q)), 0, 0],
     [0, 0, 0, 1]]
     )
  return Tx  

def roty(q):
  Ty = sp.Matrix(
    [[sp.cos(math.radians(q)), 0, sp.sin(math.radians(q)), 0],
     [0, 1, 0, 0],
     [-sp.sin(math.radians(q)), sp.cos(math.radians(q)), 0, 0],
     [0, 0, 0, 1]]
     )
  return Ty  
  
#### Frame manipulations

def toList(s):
  if "*" in s:
    return s.split("*")
  else:
    return [s]

class Frame(Node):
  def __init__(self, name, transf="identity()", **kwargs):
    super(Frame, self).__init__(str(name), **kwargs)
    self.transf = transf
    self._parseTransf()

  def _parseTransf(self):
    ts = toList(self.transf)
    H = identity()
    for t in ts:
        if t: t = eval(t)
        H *= t
    self.T = H
      
  def _post_detach(self, parent):
    pass
  
  def _post_attach(self, parent):
    pass
      
  def __repr__(self):
    s = self.name
    if self.transf: s += "("+self.transf+")"
    return s
  
#### Transformation tree

def round_expr(expr, num_digits):
  return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(sp.Number)})

class TransformationTree(object):
  def __init__(self):
    self.Hs = []
    self.root = Frame("O")
      
  def __str__(self):
    return str(RenderTree(self.root))
  
  def pos(self, v, frame):
    H = identity()
    for node in PreOrderIter(self.root):
      print node.name
      display(node.T)
      H *= node.T
      if node == frame:
          break
      #print(node.T.evalf())
    n = H*sp.Matrix(v)
    display(H)
    return n
      
  def plot_frames(self, fsize=(9,9), xl=(-2, 5),yl=(-2,5), verbose=False):
    # set up figure
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    fig = plt.figure(figsize=fsize)
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                         xlim=xl, ylim=yl)
    ax.grid()

    O_ax = sp.Matrix([0,0,0,1])
    x_ax = sp.Matrix([1,0,0,1])
    y_ax = sp.Matrix([0,1,0,1])
    z_ax = sp.Matrix([0,0,1,1])                    
    H = identity()

    cmap = plt.cm.jet
    cNorm  = colors.Normalize(vmin=0, vmax=5)

    scalarMap = cmx.ScalarMappable(norm=cNorm,cmap=cmap)

    frames = []
    for i, node in enumerate(PreOrderIter(self.root)):
      H *= node.T
      self.Hs.append(H)
      new_O = H * O_ax; v0 = map(float,new_O[:-2]) 
      new_x = H * x_ax; vx = map(float,new_x[:-2])
      new_y = H * y_ax; vy = map(float,new_y[:-2])
      new_z = H * z_ax; vz = map(float,new_z[:-2])      
      if verbose:
        print "***** Frame:",node.name
        display(round_expr(H,3))
        display(round_expr(new_O, 3))
        display(round_expr(new_x, 3))
        display(round_expr(new_y, 3))
        print "***** End frame:",node.name      
        
      colorVal = scalarMap.to_rgba(i)
      ax.arrow(v0[0],  #x1
               v0[1],  # y1
               vx[0]-v0[0], # x2 - x1
               vx[1]-v0[1], # y2 - y1
               color=colorVal, head_width=0.05, head_length=0.1)
      ax.text(vx[0],vx[1],r'$X_{%s}$'%node.name)
      ax.arrow(v0[0],  #x1
               v0[1],  # y1
               vy[0]-v0[0], # x2 - x1
               vy[1]-v0[1], # y2 - y1
               color=colorVal, head_width=0.05, head_length=0.1)
      ax.text(vy[0],vy[1],r'$Y_{%s}$'%node.name)
      
      frames.append((v0, vx, vy))

    return ax, frames


if __name__ == "__main__":
  from sympy import init_printing, pprint
  init_printing(use_latex=True) 
    
  tt = TransformationTree()
  A = Frame("A", transf="rotz(20)*transl(1,0,0)", parent=tt.root)
  B = Frame("B", transf="rotz(80)", parent=A)

  print tt

  tt.plot_frames()
  
  plt.savefig("frames.png")
  
