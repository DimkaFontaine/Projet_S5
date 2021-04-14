import os 
import sys
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O
import tools as tools
from pathlib import Path
foldername = Path(bpy.context.space_data.text.filepath)
file1 = os.path.join(foldername.parent.absolute(), 'path.py')
exec(compile(open(file1).read(), file1, 'exec'))
file2 = os.path.join(foldername.parent.absolute(), 'Car.py')
exec(compile(open(file2).read(), file2, 'exec'))
file3 = os.path.join(foldername.parent.absolute(), 'tools.py')
exec(compile(open(file2).read(), file3, 'exec'))

os.system("cls") # clean console
print("Clean objecs...")
clearMesh()      # destroy all mesh object && reset animation too the start

print("Build paths...")
curves = []
lines = []

curves.append(turnPath("curve", 0.17, 90, 'R', loc_y = 1.83))
curves.append(turnPath("curve", 0.17, 90, 'L', loc_x = 0.34, loc_y = 1.83))
curves.append(turnPath("curve", 0.17, 90, 'R', loc_x = 0.34, loc_y = 0.17))
curves[2].rotate(math.radians(90))
curves.append(turnPath("curve", 0.17, 90, 'R', loc_x = 0.34, loc_y = 0.17))
curves[3].rotate(math.radians(180))
curves.append(turnPath("curve", 0.17, 90, 'R' , loc_x = 0.68, loc_y = 0.51))
curves.append(turnPath("curve", 0.17, 90, 'R', loc_x = 1.32, loc_y = 0.85))
curves[5].rotate(math.radians(180))
curves.append(turnPath("curve", 0.17, 90, 'R', loc_x = 1.66, loc_y = 0.85))
curves.append(turnPath("curve", 0.17, 90, 'R', loc_x = 1.66, loc_y = 1.19))
curves[7].rotate(math.radians(180))
curves.append(turnPath("curve", 0.17, 90, 'L', loc_x = 2.00, loc_y = 1.49))

lines.append(straightPath("line", scale_y = 0.915))
lines.append(straightPath("line", scale_y = 0.830, loc_x = 0.34,loc_y = 0.17))
lines.append(straightPath("line", scale_y = 0.17, loc_x = 0.68, loc_y = 0.17))
lines.append(straightPath("line", scale_x = 0.32, loc_x = 0.85, loc_y = 0.68))
lines.append(straightPath("line", scale_y = 0.15, loc_x = 2,loc_y = 1.19))
lines.append(straightPath("line", scale_x = 0.575, loc_x = 0.68,loc_y = 1.66))
lines.append(straightPath("line", scale_y = 0.1, loc_x = 0.68,loc_y = 1.56))

print("Build car...")
car = Car(orientation = math.pi/2, rightLines = lines, curveLines = curves)

print("Compute car behavior...")

car.start()

print("Ready")
