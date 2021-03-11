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

def straightLineForwardTest(X,Y):
    O.mesh.primitive_plane_add() 
    C.active_object.name = "StraightLine0_4" 
    lineToCarSupport =C.active_object
    lineToCarSupport.scale = (X,Y, 0)
    lineToCarSupport.location = (0,Y,0)
    
def straightLineBackwardTest(X,Y):
    O.mesh.primitive_plane_add() 
    C.active_object.name = "StraightLine-4_0" 
    lineToCarSupport =C.active_object
    lineToCarSupport.scale = (X,Y, 0)
    lineToCarSupport.location = (0,-Y,0)
    
def straightLineForwardWithObstacleTest(X,Y):
    straightLineForwardTest(X,Y)
    O.mesh.primitive_cube_add() 
    C.active_object.name = "Obstacle" 
    lineToCarSupport =C.active_object
    lineToCarSupport.scale = (X, X, 0.5)
    lineToCarSupport.location = (0,(Y*2),0)

def straightLineForwardWithObstacleInMiddleTest(X,Y):
    straightLineForwardTest(X,Y)
    O.mesh.primitive_cube_add() 
    C.active_object.name = "Obstacle" 
    lineToCarSupport =C.active_object
    lineToCarSupport.scale = (X, X, 0.5)
    lineToCarSupport.location = (0,Y,0)

def leftCurve():
    O.mesh.primitive_plane_add()  
    path1 = C.active_object
    path1.scale = (5.0, 5.0, 1.0)
    path1.location = (0.0, 5.0, 0.0)
    
    bpy.ops.mesh.primitive_cylinder_add() 
    C.active_object.name = "Hole maker" 
    hole_maker = C.active_object
    hole_maker.scale = (4.991, 4.991, 1.0) 
    hole_maker.location = (-5.0, 0.0, 0.0) 
    
    makeHole(path1, hole_maker)
    
    hole_maker = C.active_object
    hole_maker.scale = (5.009, 5.009, 1.0)
    
    makeIntersect(path1, hole_maker)
    
    O.object.select_all(action='DESELECT')
    path1.select_set(False)
    D.objects['Hole maker'].select_set(True)
    O.object.delete()
    

def rightCurve():
    O.mesh.primitive_plane_add()  
    path1 = C.active_object
    path1.scale = (5.0, 5.0, 1.0)
    path1.location = (0.0, 5.0, 0.0)
    
    bpy.ops.mesh.primitive_cylinder_add() 
    C.active_object.name = "Hole maker" 
    hole_maker = C.active_object
    hole_maker.scale = (4.991, 4.991, 1.0) 
    hole_maker.location = (5.0, 0.0, 0.0) 
    
    makeHole(path1, hole_maker)
    
    hole_maker = C.active_object
    hole_maker.scale = (5.009, 5.009, 1.0)
    
    makeIntersect(path1, hole_maker)
    
    O.object.select_all(action='DESELECT')
    path1.select_set(False)
    D.objects['Hole maker'].select_set(True)
    O.object.delete()

def tightLeftCurve():
    O.mesh.primitive_plane_add()  
    path1 = C.active_object
    path1.scale = (1.2, 1.2, 1.0)
    path1.location = (0.0, 1.2, 0.0)
    
    bpy.ops.mesh.primitive_cylinder_add() 
    C.active_object.name = "Hole maker" 
    hole_maker = C.active_object
    hole_maker.scale = (1.191, 1.191, 1.0) 
    hole_maker.location = (-1.2, 0.0, 0.0) 
    
    makeHole(path1, hole_maker)
    
    hole_maker = C.active_object
    hole_maker.scale = (1.209, 1.209, 1.0)
    
    makeIntersect(path1, hole_maker)
    
    O.object.select_all(action='DESELECT')
    path1.select_set(False)
    D.objects['Hole maker'].select_set(True)
    O.object.delete()
    
   
def tightRightCurve():
    O.mesh.primitive_plane_add()  
    path1 = C.active_object
    path1.scale = (1.2, 1.2, 1.0)
    path1.location = (0.0, 1.2, 0.0)
    
    bpy.ops.mesh.primitive_cylinder_add() 
    C.active_object.name = "Hole maker" 
    hole_maker = C.active_object
    hole_maker.scale = (1.191, 1.191, 1.0) 
    hole_maker.location = (1.2, 0.0, 0.0) 
    
    makeHole(path1, hole_maker)
    
    hole_maker = C.active_object
    hole_maker.scale = (1.209, 1.209, 1.0)
    
    makeIntersect(path1, hole_maker)
    
    O.object.select_all(action='DESELECT')
    path1.select_set(False)
    D.objects['Hole maker'].select_set(True)
    O.object.delete()
    

print("Reset") 

clearMesh()      # destroy all mesh object && reset animation too the start
os.system("cls") # clean console

print() 
print("Start") 

path = tightRightCurve()

print("end")