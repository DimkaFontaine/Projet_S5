#//////////////////////         Imports          ////////////////////////////////////
import os 
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 

#//////////////////////         Functions          ////////////////////////////////////
def clearMesh():
    bpy.ops.screen.animation_cancel(restore_frame=True)
    for o in bpy.context.scene.objects: 
        if o.type == 'MESH': 
            o.select_set(True) 
        else: 
            o.select_set(False)
    bpy.ops.object.delete() 


def addVec3(a,b):
    c = [0.0,0.0,0.0]
    c[0] = a[0] + b[0]
    c[1] = a[1] + b[1]
    c[2] = a[2] + b[2] 
    return c

def minusVec3(a,b):
    c = [0.0,0.0,0.0]
    c[0] = a[0] - b[0]
    c[1] = a[1] - b[1]
    c[2] = a[2] - b[2] 
    return c

def distance3(vector):
    return pow((pow(vector[0],2)+pow(vector[1],2))+pow(vector[2],2),0.5)


# sensorFeedback(sensor, orientation, colliders)
#   -description:
#       simulate the behavior of a sensor A.K.A Usful and usable raycasting
#   -param:
#       sensor: 
#           mesh object that simulates the sensor
#       orientation: 
#           the orientation that we want it to detect, in relation to the world (independent of the orientation of the sensor)
#       colliders:
#           list of objects that we want to be able to detect
#   -return:
#       [0] : name of the object detected (None if not detected)
#       [1] : distance of the object detected (-1 if not detected)
#
def sensorFeedback(sensor, orientation, colliders): 
    for col in colliders: 
        loc = [sensor.location[0]-col.location[0],sensor.location[1]-col.location[1],sensor.location[2]-col.location[2]]
        results = col.ray_cast(loc, orientation) 
        if results[0]: 
            q = addVec3(col.location,results[1])
            v = minusVec3(q,sensor.location)
            d = distance3(v)
            return [col.name,d] 
    return [None,-1.0]

#//////////////////////         Constants          ////////////////////////////////////

frames = 250 
speed = -6.0*(1.0/24.0)

#//////////////////////         Script          ////////////////////////////////////


print("Reset") 

clearMesh()      # destroy all mesh object && reset animation too the start
os.system("cls") # clean console

print() 
print("Start") 

# Floor
bpy.ops.mesh.primitive_plane_add(size=100, location=(0.0, 0.0, -1.0)) 
C.active_object.name = "Floor"

# Obstacles
bpy.ops.mesh.primitive_cube_add(size=5, location=(-10.0, 5.0, 0.0), scale=(3.0,1.0,1.0)) 
C.active_object.name = "Bloc0" 
bloc0 =C.active_object
 
bpy.ops.mesh.primitive_cube_add(location=(-40.0, 0.0, 0.0)) 
C.active_object.name = "Bloc1" 
bloc1 =C.active_object 
colliders = [bloc0,bloc1]

# Sensor
bpy.ops.mesh.primitive_cube_add() 
C.active_object.name = "Sensor"
ob = C.active_object 



for i in range(frames): 
    
    C.scene.frame_set(i) 
    
    # check for collision
    detected = sensorFeedback(ob,[-1.0,0.0,0.0],colliders)


    if(detected[1]<10 and detected[0] is not None):   #if detected and distance < 10 => go backwards
        print("DETECTED: ", detected[0]) 
        speed = -speed
    
    if i>5 and ob.location[0]>-0.01:    #if at start position => stop        
        speed=0
    
    #update location and add keyframe
    ob.location[0] = ob.location[0]+ speed
    bpy.ops.anim.keyframe_insert(type = 'LocRotScale') 
        
# Play
bpy.ops.screen.animation_play() 