import os 
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O

def clearMesh():
    bpy.ops.screen.animation_cancel(restore_frame=True)
    for o in bpy.context.scene.objects: 
        if o.type == 'MESH': 
            o.select_set(True) 
        else: 
            o.select_set(False)
    bpy.ops.object.delete() 
    
    
def makeHole(main, hole):
    bpy.ops.object.select_all(action='DESELECT')
    main.select_set(True)
    bool_one = main.modifiers.new(type="BOOLEAN", name="Boolean")
    bool_one.solver = 'FAST'
    bool_one.object = hole
    bool_one.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply({"object": main},modifier="Boolean")
    return   

def makeIntersect(main, intersect):
    bpy.ops.object.select_all(action='DESELECT')
    main.select_set(True)
    bool_one = main.modifiers.new(type="BOOLEAN", name="Boolean")
    bool_one.solver = 'FAST'
    bool_one.object = intersect
    bool_one.operation = 'INTERSECT'
    bpy.ops.object.modifier_apply({"object": main},modifier="Boolean")
    return  

def straightPath(name, scale_x = 0.009,scale_y = 0.009, loc_x =0, loc_y =0):
    O.mesh.primitive_plane_add()
    C.active_object.name = name
    path =C.active_object
    path.scale = (scale_x,scale_y, 0)
    path.location = (loc_x, loc_y,0)
    
    return path
    
    
    #direction L = left
    #          R = right
def turnPath(name, radius, direction = 'L', loc_x =0, loc_y =0):
    O.mesh.primitive_plane_add()  
    path = C.active_object
    C.active_object.name = name
    path.scale = (radius, radius, 1.0)
    path.location = (0.0, radius, 0.0)
    
    bpy.ops.mesh.primitive_cylinder_add(vertices = 128) 
    C.active_object.name = "Hole maker" 
    hole_maker = C.active_object
    hole_maker.scale = ((radius - 0.009), (radius - 0.009), 1.0) 
    
    if direction == 'L':
        direction_location = radius * -1
    else:
        direction_location = radius
    
    hole_maker.location = (direction_location , 0.0, 0.0)
    
    makeHole(path, hole_maker)
    
    hole_maker = C.active_object
    hole_maker.scale = ((radius + 0.009), (radius + 0.009), 1.0)
    
    makeIntersect(path, hole_maker)
    
    O.object.select_all(action='DESELECT')
    path.select_set(False)
    D.objects['Hole maker'].select_set(True)
    O.object.delete() 
    
    return path
    

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
    turnPath("leftTest", 0.12, direction = 'L')
    

def rightCurveTest():
    turnPath("rightTest", 0.5, direction = 'R')

def tightLeftCurveTest():
    turnPath("leftTightTest", 0.12, direction = 'L')
    
   
def tightRightCurveTest():
    turnPath("rightTightTest", 0.12, direction = 'R')
print("Reset") 

clearMesh()      # destroy all mesh object && reset animation too the start
os.system("cls") # clean console

print() 
print("Start") 

rightCurveTest()

print("end")