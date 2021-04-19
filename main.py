import os 
import sys
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O
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
obstacles = []

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

bpy.ops.mesh.primitive_cube_add() 
C.active_object.name = "Obs" 
obs =C.active_object
obs.dimensions = (0.075, 0.064, 0.115)
obs.location = (0.34,0.6,0.115/2)
obstacles.append(obs)
bpy.ops.mesh.primitive_cube_add() 
C.active_object.name = "Obs1" 
obs1 =C.active_object
obs1.dimensions = (0.064, 0.075, 0.115)
obs1.location = (1.2,0.68,0.115/2)
obstacles.append(obs1)
bpy.ops.mesh.primitive_cube_add() 
C.active_object.name = "Obs2" 
obs2 =C.active_object
obs2.dimensions = (0.064, 0.075, 0.115)
obs2.location = (1.3,1.66,0.115/2)
obstacles.append(obs2)

print("Build car...")
car = Car(orientation = math.pi/2, rightLines = lines, curveLines = curves, obstacles = obstacles)

print("Compute car behavior...")

car.start()

print("Ready")
