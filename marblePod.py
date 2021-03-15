import os 
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O

os.system("cls") # clean console 

def clearMesh():
    bpy.ops.screen.animation_cancel(restore_frame=True)
    O.object.select_all(action='DESELECT')
    for o in bpy.context.scene.objects: 
        if o.type == 'MESH': 
            o.select_set(True) 
        elif o.name == 'MarblePod':
            o.select_set(True)
        else: 
            o.select_set(False)
    bpy.ops.object.delete() 
    
    
class MarblePod:
        def __init__(self, location = (0.0,0.0)):
            self.location = location
            self.buildMarblePod()
            
        def buildMarblePod(self):
        
            def buildPod(self):
                O.mesh.primitive_cube_add(location = (self.location[1],self.location[2],self.location[2] -0.0005), scale = (0.05, 0.05, 0.004))  
                pod = C.active_object
                hole = buildHoleSolid(self)
                makeHole(pod, hole, 'Hole Solid')
                pod.select_set(True)
                setMaterial(pod, makeMaterial('Red',(0.5,0,0,0.95),(1,1,1)))
                return pod
            
            def makeMaterial(name, diffuse, specular):
                mat = bpy.data.materials.new(name)
                mat.diffuse_color = diffuse
                mat.specular_color = specular
                mat.specular_intensity = 0.5
                return mat
            
            def setMaterial(ob, mat):
                me = ob.data
                me.materials.append(mat)
                
            def makeHole(main, hole, holeMakerName):
                bpy.ops.object.select_all(action='DESELECT')
                main.select_set(True)
                bool_one = main.modifiers.new(type="BOOLEAN", name="Boolean")
                bool_one.object = hole
                bool_one.operation = 'DIFFERENCE'
                bpy.ops.object.modifier_apply({"object": main},modifier="Boolean")
                O.object.select_all(action='DESELECT')
                D.objects[holeMakerName].select_set(True)
                O.object.delete()
                return  
    
            def buildHoleSolid(self):
                O.mesh.primitive_uv_sphere_add(ring_count = 256, segments = 256, location = (self.location[1],self.location[2],self.location[3] + 0.14), scale = (0.28,0.28,0.28))
                holeSolid = C.active_object
                holeMakerName = 'Hole Solid'
                C.active_object.name = holeMakerName 
                return holeSolid   
            
            def buildMarble(self):
                O.mesh.primitive_uv_sphere_add(ring_count = 64, segments = 64, location = (self.location[1],self.location[2],self.location[3] + 0.0075), scale = (0.015,0.015,0.015))
                marble = C.active_object
                marbleName = 'Marble'
                C.active_object.name = marbleName
                setMaterial(marble, makeMaterial('Blue',(0,0,0.5,1),(1,1,1)))
                return marble
            
            buildPod(self)
            buildMarble(self)

clearMesh()            
     
marblePod = MarblePod(location = (0,0,0,0))