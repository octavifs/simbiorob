#!/usr/bin/python

import frames 
import sympy as sp

class Link(frames.Frame):
    def __init__(self, lid, l, angle):
        self.lid = lid
        self.l = l
        self.angle = angle
        t = "rotz(%.2f)"%angle
        super(Link, self).__init__(lid, transf=t)
  
    def _post_attach(self, parent):
        if isinstance(parent, Link):
            self.transf = "transl(%.2f,.0,.0)"%parent.l + "*" + self.transf
            #print "New transf", self.transf
            self._parseTransf()
    
class MultiLink(object):
    def __init__(self):
        self.tt = frames.TransformationTree()
        self.links = []

    def addLink(self, v, angle):
        p = self.tt.root
        if self.links: p=self.links[-1]
        l = Link("l%d"%len(self.links),v, angle)
        l.parent = p
        self.links.append(l)
        return l

    def plotInFrame(self, v, ax, frame_id):
        O_ax = sp.Matrix([0,0,0,1])
        v = sp.Matrix(v)
        NO_ax = self.tt.Hs[frame_id]*O_ax
        Nv = self.tt.Hs[frame_id]*v     
        ax.plot( (NO_ax[0], Nv[0]), (NO_ax[1], Nv[1]), 'o-', lw=4, mew=5, alpha=0.7)
    
    def plotLinks(self):
        ax, _ = self.tt.plot_frames(xl=(-1, 6),yl=(-1,6))
        for i,link in enumerate(self.links):
            self.plotInFrame([link.l, 0, 0, 1], ax,i+1)
    
if __name__ == '__main__':
  from sympy import init_printing, pprint
  init_printing() 

  l1 = 1.0; a1 = 45.0
  l2 = 2.0; a2 = -10.0
  l3 = 3.0; a3 = 10.0
  arm = MultiLink()
  link1 = arm.addLink(l1, a1)
  link2 = arm.addLink(l2, a2)
  link3 = arm.addLink(l3, a3)
  print arm.tt

  arm.plotLinks()
  
  plt.savefig("links.png")

