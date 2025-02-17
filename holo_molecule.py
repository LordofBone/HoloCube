#credit to pi3d demos for majority of the code - view the license here for the original repo https://github.com/pi3d/pi3d_demos/blob/master/LICENSE
#this has been edited by me to render the molecule as a 3D pyramid hologram

#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
""" An example of making objects change shape using Buffer.re_init().
It shows how a subset of vertices can be altered
"""
from math import sin, cos, radians
from time import time
import random

import demo
import pi3d
import json

DISPLAY = pi3d.Display.create(w=800, h=480, background=(0.0, 0.0, 0.0, 1.0))

CAMERA = pi3d.Camera()

#added these in to scale the size of the individual atoms and distance from each other down to suit the smaller screen
scaleDownFactor = 6
scaleDownFactorAtom = 5

''' Demonstration of MergeShape using child objects as had to be done to
give different materials prior to pi3d v.2.22
 
ADP-glucose C16H25N5O15P2 from pubchem.ncbi.nlm.nih.gov
'''
with open('models/Structure3D_CID_16500.json','r') as f:
  json_data = json.load(f)['PC_Compounds'][0]
element = json_data['atoms']['element']
x = json_data['coords'][0]['conformers'][0]['x']
y = json_data['coords'][0]['conformers'][0]['y']
z = json_data['coords'][0]['conformers'][0]['z']
n = len(element)
'''NB if you download different molecules you might need to add to alter this.
 atomic number: name, radius, (r,g,b) tuple '''
atoms = {1:['hydrogen', 0.5/scaleDownFactorAtom, (1.0, 0.0, 0.0)],
         6:['carbon', 0.8/scaleDownFactorAtom, (0.1, 0.1, 0.1)],
         7:['nitrogen', 0.9/scaleDownFactorAtom, (0.1, 0.9, 1.0)],
         8:['oxygen', 0.9/scaleDownFactorAtom, (1.0, 1.0, 1.0)],
         15:['phosphorus', 1.5/scaleDownFactorAtom, (1.0, 0.0, 1.0)]}

shape1 = pi3d.Sphere(radius=atoms[6][1], y=2.5)

empty = pi3d.Triangle(corners=((-0.01, 10.0), (0.0, 0.01), (0.01, 0.0)), z=10.0)

elem = {}

#made some changes here to make the elem variable a list so that each individual set of atoms can be manipulated later on
#otherwise the elem variable will overwrite itself on each atom iteration and only the last set will be manipulable
for e in atoms:
  if e != 6: # don't do carbon again
    shape1 = pi3d.Sphere(radius=atoms[e][1])
    elem[e] = pi3d.MergeShape()
    
    for i in range(n):
      if element[i] == e:
        elem[e].add(shape1, x[i]/scaleDownFactor, y[i]/scaleDownFactor, z[i]/scaleDownFactor)
    elem[e].set_material(atoms[e][2])
	#move the elem on the Y access so that it will be moved to a good location on the screen for the pyramid
    elem[e].positionY(2.0)
    empty.add_child(elem[e])

keys = pi3d.Keyboard()
mouse = pi3d.Mouse(restrict=False)
mouse.start()

# rotations for camera views ry, rz
views = ((0.0, 0.0), 
         (-90.0, 90.0), 
         (90.0, -90), 
         (180.0, 180.0))
         
while DISPLAY.loop_running():
  
  mx, my = mouse.position()

  rot = - mx * 0.2
  tilt = my * 0.2
  
  #rotate each set of atoms to the position of the mouse, avoiding no.6 as carbon is not used
  for e in atoms:
    if e != 6:
		elem[e].rotateToY(rot)
		elem[e].rotateToX(tilt)
  
  #rotate the entire rendering to different angles and on different parts of the screen for each side of the pyramid
  for v in views:
    empty.rotateToY(v[0])
    empty.rotateToZ(v[1])
    empty.draw()

  if keys.read() == 27:
    break
