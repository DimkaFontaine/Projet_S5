import os 
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O
foldername = bpy.context.space_data.text.filepath[0:-12]

file = os.path.join(foldername, 'tools.py')
exec(compile(open(file).read(), file, 'exec'))


os.system("cls") # clean console 
    
    
class MarblePod:
        def __init__(self, location = (0.0,0.0,0.0)):
            self.location = location
            self.buildMarblePod()
            
        def buildMarblePod(self):
        
            def buildPod(self):
                O.mesh.primitive_cube_add(location = (self.location[0],self.location[1],self.location[2] -0.0005), scale = (0.05, 0.05, 0.004))  
                O.rigidbody.object_add()
                C.object.rigid_body.type = 'PASSIVE'
                pod = C.active_object
                podName = 'Pod'
                C.active_object.name = podName
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
                
            def buildHoleSolid(self):
                O.mesh.primitive_uv_sphere_add(ring_count = 256, segments = 256, location = (self.location[0],self.location[1],self.location[2] + 0.14), scale = (0.28,0.28,0.28))
                holeSolid = C.active_object
                holeMakerName = 'Hole Solid'
                C.active_object.name = holeMakerName 
                return holeSolid   
            
            def buildMarble(self):
                O.mesh.primitive_uv_sphere_add(ring_count = 64, segments = 64, location = (self.location[0],self.location[1],self.location[2] + 0.0075), scale = (0.015,0.015,0.015))
                O.rigidbody.object_add()
                C.object.rigid_body.collision_shape = 'MESH'
                marble = C.active_object
                marbleName = 'Marble'
                C.active_object.name = marbleName
                setMaterial(marble, makeMaterial('Blue',(0,0,0.5,1),(1,1,1)))
                return marble
            
            buildPod(self)
            buildMarble(self)