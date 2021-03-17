import os 
import sys
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O


def clearMesh():
    bpy.ops.screen.animation_cancel(restore_frame=True)
    O.object.select_all(action='DESELECT')
    for o in bpy.context.scene.objects: 
        if o.type == 'MESH': 
            o.select_set(True) 
        elif o.name == 'Car':
            o.select_set(True)
        else: 
            o.select_set(False)
    bpy.ops.object.delete() 
    


os.system("cls") # clean console
print("Clean objecs...")
clearMesh()      # destroy all mesh object && reset animation too the start

print("Load files...")
foldername =bpy.context.space_data.text.filepath[0:-7]
file1 = os.path.join(foldername, 'path.py')
exec(compile(open(file1).read(), file1, 'exec'))
file2 = os.path.join(foldername, 'Car.py')
exec(compile(open(file2).read(), file2, 'exec'))

print("Build paths...")
curves = []
lines = []

curves.append(turnPath("leftTest", 0.36, 90, direction = 'L'))
curves.append(turnPath("leftTest", 0.36, 90, direction = 'L'))

lines.append(straightPath("StraightLineForward", scale_y = 1, loc_y = 0))
lines.append(straightPath("StraightLineForward", scale_y = 1, loc_y = 0))

lines[1].location = (-0.72,3.72,0.0)

curves[0].move(0.0,2)
curves[1].move(0,2.72)
curves[1].rotate(math.pi)

print("Build car...")
car = Car(orientation = math.pi/2, rightLines = lines, curveLines = curves)


print("Compute car behavior...")
    
frames = 800
C.scene.frame_end = frames

car.setSpeed(50)

for i in range(frames): 
    
    C.scene.frame_set(i) 
    car.update1in24frame() 
    r = car.detectLigne()     
    if r[0]:
        car.setWheels(0)
    if r[4]:
        car.setWheels(180)
    if r[1]:
        car.setWheels(70)
    if r[3]:
        car.setWheels(110)

print("Ready")