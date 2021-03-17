import os 
import math 
import bpy 
import sys
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O
foldername = bpy.context.space_data.text.filepath[0:-7]
file = os.path.join(foldername, 'tools.py')
exec(compile(open(file).read(), file, 'exec'))


class curvePath:
    def __init__(self,object,center,radius,angle,orientation):
        self.object = object
        self.center = center
        self.centerWorld = [object.location[0] + center[0],object.location[1] + center[1]]
        self.radius= radius
        self.angle = angle
        self.orientation = orientation
        
    def rotate(self,angle):
        self.object.rotation_euler[2] = self.object.rotation_euler[2]+ angle
        newCenter = [self.center[0]*math.cos(angle) -self.center[1]*math.sin(angle), self.center[0]*math.sin(angle) +self.center[1]*math.cos(angle)]
        deplacement = [newCenter[0] - self.center[0],newCenter[1] - self.center[1]]
        self.object.location[0] = self.object.location[0]-deplacement[0]
        self.object.location[1] = self.object.location[1]-deplacement[1]
        self.center = newCenter
        self.centerWorld = [self.object.location[0] + self.center[0],self.object.location[1] + self.center[1]]
        self.orientation = self.orientation + angle

    def move(self,x,y):
        self.object.location[0] = self.object.location[0]+x
        self.object.location[1] = self.object.location[1]+y
        self.centerWorld = [self.object.location[0] + self.center[0],self.object.location[1] + self.center[1]]


def straightPath(name, scale_x = 0.009,scale_y = 0.009, loc_x =0, loc_y =0):
    O.mesh.primitive_plane_add()
    C.active_object.name = name
    path =C.active_object
    path.scale = (scale_x,scale_y, 0)
    
    if scale_x > scale_y:
        direction_x = scale_x
        direction_y = 0
    else : 
        direction_x = 0
        direction_y = scale_y
    
    path.location = (loc_x + direction_x, loc_y + direction_y,0)
    return path
    
    #direction L = left
    #          R = right
def turnPath(name, radius, angle, direction = 'L',loc_x =0, loc_y =0):
    if direction == 'L':
        direction_factor =-1
        angle_offset= 270
    else:
        angle_offset= 90
        direction_factor = 1
    
    #Create path plane
    O.mesh.primitive_plane_add()  
    path = C.active_object
    C.active_object.name = name
    path.scale = (radius, radius, 1.0)
    path.location = (loc_x, loc_y + radius, 0.0)
    
    #Create a cylinder to cut the plane inner radius
    bpy.ops.mesh.primitive_cylinder_add(vertices = 128) 
    C.active_object.name = "Hole maker" 
    hole_maker = C.active_object
    hole_maker.scale = ((radius - 0.009), (radius - 0.009), 1.0) 
    
    #Rescle the cylinder to cut the outer radius 
    hole_maker.location = ((direction_factor*radius) + loc_x , loc_y, 0.0)
    
    center = [hole_maker.location[0]-path.location[0],hole_maker.location[1]-path.location[1]]
    
    makeHole(path, hole_maker)
    
    hole_maker = C.active_object
    hole_maker.scale = ((radius + 0.009), (radius + 0.009), 1.0)
    
    makeIntersect(path, hole_maker, 'Hole maker')
    
    #Create cube to cut the path at the right angle
    bpy.ops.mesh.primitive_cube_add() 
    C.active_object.name = "Angle maker" 
    angle_maker = C.active_object
    angle_maker.scale = ((radius+1), 2*radius, 1.0)
    angle_maker.location = ((direction_factor*radius) + loc_x, loc_y , 0)
    
    bpy.ops.mesh.primitive_cube_add() 
    C.active_object.name = "Hole maker2" 
    hole_maker2 = C.active_object
    hole_maker2.scale = (radius, (2*radius+0.1), 1.1)
    hole_maker2.location = (loc_x, loc_y, 0.0)
    
    makeHole(angle_maker, hole_maker2, 'Hole maker2')

    #Rotate and cut
    angle_maker.rotation_euler = (0,0,math.radians(angle_offset-(angle*direction_factor)))
    makeHole(path, angle_maker, 'Angle maker')
    
    p = curvePath(path,center,radius, math.radians(angle),0)
    
    return p
    

#test path creation functions  

def straightLineForwardTest():
    straightPath("StraightLineForward", scale_y = 1, loc_y = 1)
    
    
def straightLineBackwardTest():
    straightPath("StraightLineBackward", scale_y = 1, loc_y = 1)
    
def straightLineForwardWithObstacleTest():
    straightPath("StraightLineForward", scale_y = 1, loc_y = 1)
    O.mesh.primitive_cube_add() 
    C.active_object.name = "Obstacle" 
    lineToCarSupport =C.active_object
    lineToCarSupport.scale = (0.01, 0.01, 0.5)
    lineToCarSupport.location = (0,2,0)

def straightLineForwardWithObstacleInMiddleTest():
    straightPath("StraightLineForward", scale_y = 1, loc_y = 1)
    O.mesh.primitive_cube_add() 
    C.active_object.name = "Obstacle" 
    lineToCarSupport =C.active_object
    lineToCarSupport.scale = (0.01, 0.01, 0.5)
    lineToCarSupport.location = (0,1,0)

def leftCurveTest():
    turnPath("leftTest", 0.12, 90, direction = 'L')
    

def rightCurveTest():
    turnPath("rightTest", 0.5, 90, direction = 'R')

def tightLeftCurveTest():
    turnPath("leftTightTest", 0.12, 90, direction = 'L')
    
   
def tightRightCurveTest():
    turnPath("rightTightTest", 0.12, 90, direction = 'R')
    
    
#print("Reset") 

#clearMesh()      # destroy all mesh object && reset animation too the start
#os.system("cls") # clean console

#tightRightCurveTest()
