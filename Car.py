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






def buildCar():
    
    def makeHole(main, hole):
    
        bpy.ops.object.select_all(action='DESELECT')
        main.select_set(True)
        bool_one = main.modifiers.new(type="BOOLEAN", name="Boolean")
        bool_one.object = hole
        bool_one.operation = 'DIFFERENCE'
        bpy.ops.object.modifier_apply({"object": main},modifier="Boolean")
        return    
    
    def makePoll():
        O.mesh.primitive_cylinder_add()  
        poll = C.active_object
        poll.delta_scale = (0.01, 0.01, 0.06)
        poll.rotation_euler = (math.pi/2,0.0,0.0)
        return poll
    
    def makeWheel():
        O.mesh.primitive_cylinder_add()  
        wheel = C.active_object
        wheel.delta_scale = (0.0325, 0.0325, 0.0125)
        wheel.rotation_euler = (math.pi/2,0.0,0.0)
        return wheel
    
#    carCollection = bpy.data.collections.new('Car')
#    bpy.context.scene.collection.children.link(carCollection)
#    
#    layer_collection = bpy.context.view_layer.layer_collection.children[carCollection.name]
#    bpy.context.view_layer.active_layer_collection = layer_collection
    
    # Build main body
    bpy.ops.mesh.primitive_cube_add() 
    C.active_object.name = "Body" 
    body =C.active_object
    body.delta_scale = (0.12, 0.045, 0.045)
    
    # Build holes for the wheels
    bpy.ops.mesh.primitive_cylinder_add() 
    C.active_object.name = "Hole maker" 
    hole_maker =C.active_object
    hole_maker.delta_scale = (0.05, 0.05, 0.02)
    hole_maker.rotation_euler = (math.pi/2,0.0,0.0)
    hole_maker.location = (0.08,0.045,-0.035)
    makeHole(body, hole_maker)
    hole_maker.location = (0.08,-0.045,-0.035)
    makeHole(body, hole_maker)
    hole_maker.location = (-0.08,0.045,-0.035)
    makeHole(body, hole_maker)
    hole_maker.location = (-0.08,-0.045,-0.035)
    makeHole(body, hole_maker)
    O.object.select_all(action='DESELECT')
    body.select_set(False)
    D.objects['Hole maker'].select_set(True)
    O.object.delete()
    
    # Build polls
    poll1 = makePoll()
    C.active_object.name = "Poll1" 
    poll1.location = (0.08,0.0,-0.035)
    poll2 = makePoll()
    C.active_object.name = "Poll2" 
    poll2.location = (-0.08,0.0,-0.035)

    # Build wheels
    wheelFR =  makeWheel()
    C.active_object.name = "WheelFR" 
    wheelFR.location = (0.08,-0.06,-0.035)
    wheelFL =  makeWheel()
    C.active_object.name = "WheelFL" 
    wheelFL.location = (0.08,0.06,-0.035)
    wheelBR =  makeWheel()
    C.active_object.name = "WheelBR" 
    wheelBR.location = (-0.08,-0.06,-0.035)
    wheelBL =  makeWheel()
    C.active_object.name = "WheelBL" 
    wheelBL.location = (-0.08,0.06,-0.035)
    

print("Reset") 

clearMesh()      # destroy all mesh object && reset animation too the start
os.system("cls") # clean console

print() 
print("Start") 

car = buildCar()

print("end")
#bpy.ops.outliner.item_activate(extend=False, deselect_all=True)
#bpy.context.space_data.context = 'OBJECT'
#bpy.context.object.location[0] = 0.11
#bpy.context.space_data.context = 'MODIFIER'
#bpy.ops.object.modifier_add(type='BOOLEAN')
#bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Cylinder"]
#bpy.ops.object.modifier_apply(modifier="Boolean")