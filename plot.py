#Based on code by Travis DeWolf - https://studywolf.wordpress.com/
import numpy as np
import matplotlib.pyplot as plt
from links import Link, MultiLink
import transf as t
import math
import sympy as sp

np.set_printoptions(precision=3, suppress=True)  # neat printing

def perpendicular(a) :
  b = np.empty_like(a)
  b[0] = -a[1]
  b[1] = a[0]
  return b
  
def normalize(a):
  a = np.array(a)
  return a/np.linalg.norm(a)  

def plot_refs(v0, v1, ax):
  v = normalize(v1 - v0)
  p = perpendicular(v)
  xRef = np.concatenate((v0, v))
  yRef = np.concatenate((v0, p))
  ax.arrow(*xRef, head_width=0.05, head_length=0.1)
  ax.arrow(*yRef, head_width=0.05, head_length=0.1)

def plot_links(links, fsize=(4,4), xl=(-2, 5),yl=(-2, 5)):
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
    
    line, = ax.plot( (v0[0], v1[0]), (v0[1], v1[1]), 'o-', lw=4, mew=5, alpha=0.7)
    plot_refs(np.asarray(v0), np.asarray(v1), ax)

    lO = nO    

  return ax
  
if __name__ == "__main__":
 
  sp.init_printing() 
  
  l = 1.0

  arm = MultiLink()  
  arm.add_link(l,t.zaxis,0)
  arm.add_link(l,t.zaxis,90)
  arm.add_link(l,t.zaxis,0)  
  
  #for l in arm.links:
  #  sp.pprint(l.getHSym())
  
  sp.pprint(arm.compose(sym=True))
  
  ax = plot_links(arm.getLinks())

  lO = sp.Matrix([0,0,0,1])
  nO = sp.Matrix(arm.compose()*lO)
  v0 = map(float,lO[:-2]); 
  v1 = map(float,nO[:-2]);  

  sp.pprint(v0)
  sp.pprint(v1)  
  ax.plot( (v0[0], v1[0]), (v0[1], v1[1]),"k")
  
  plt.savefig("t1.png")
  
