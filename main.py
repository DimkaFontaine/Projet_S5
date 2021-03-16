import os 
import sys
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O
foldername =bpy.context.space_data.text.filepath[0:-7]
file1 = os.path.join(foldername, 'path.py')
exec(compile(open(file1).read(), file1, 'exec'))
file2 = os.path.join(foldername, 'Car.py')
exec(compile(open(file2).read(), file2, 'exec'))

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
    
    
clearMesh()      # destroy all mesh object && reset animation too the start
os.system("cls") # clean console

 
straightPath("test", scale_y = 1)
testModelisation()

#car = Car(orientation = math.radians(90))
#car.setSpeed(100)