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
    
def makeHole(main, hole, holeMakerName = ''):
    bpy.ops.object.select_all(action='DESELECT')
    main.select_set(True)
    bool_one = main.modifiers.new(type="BOOLEAN", name="Boolean")
    bool_one.solver = 'FAST'
    bool_one.object = hole
    bool_one.operation = 'DIFFERENCE'
    bpy.ops.object.modifier_apply({"object": main},modifier="Boolean")
                
    if holeMakerName != '':
        O.object.select_all(action='DESELECT')
        D.objects[holeMakerName].select_set(True)
        O.object.delete()
    return 

def makeIntersect(main, intersect, holeMakerName = ''):
    bpy.ops.object.select_all(action='DESELECT')
    main.select_set(True)
    bool_one = main.modifiers.new(type="BOOLEAN", name="Boolean")
    bool_one.solver = 'FAST'
    bool_one.object = intersect
    bool_one.operation = 'INTERSECT'
    bpy.ops.object.modifier_apply({"object": main},modifier="Boolean")
    
    if holeMakerName != '':
        O.object.select_all(action='DESELECT')
        D.objects[holeMakerName].select_set(True)
        O.object.delete()
    return                 