import os 
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O

from pathlib import Path
foldername = Path(bpy.context.space_data.text.filepath)
file = os.path.join(foldername.parent.absolute(), 'tools.py')
exec(compile(open(file).read(), file, 'exec'))


os.system("cls") # clean console 
    
# MarblePod
#   -description:
#       Permet d'instancier la nacelle de la bille avec les propriété physiques nécessaire à la simulation
#   -param:
#       -location: Coordonnés initiales (x,y,z)
#   -return: MerblePod
class MarblePod:
        def __init__(self, location = (0.0,0.0,0.0)):
            self.location = location
            self.r = 0.0075
            self.marbleOnPod = True
            self.pod = self.buildPod()
            self.marble = self.buildMarble()
            O.object.select_all(action='DESELECT')
            self.pod.location = (0.0,0.0,0.0)
            self.marble.location = (0.0,0.0,self.r)
            self.marbleForceVec = [0.0,0.0,0.0]
            
            
        def addMarbleForce(self, V3 = [0.0,0.0,0.0]):
            self.marbleForceVec[0] = self.marbleForceVec[0] + V3[0]
            self.marbleForceVec[1] = self.marbleForceVec[1] + V3[1]
            self.marbleForceVec[2] = self.marbleForceVec[2] + V3[2]
            
        
        def initMove(self,loc):
            self.pod.location[0] = loc[0]
            self.pod.location[1] = loc[1]
            self.pod.location[2] = loc[2]
            self.marble.location[2] = loc[2] + self.r
            self.marble.location[0] = loc[0]
            self.marble.location[1] = loc[1]
            
        
        def buildPod(self):
            O.mesh.primitive_cube_add(location = (self.location[0],self.location[1],self.location[2] -0.0005), scale = (0.05, 0.05, 0.004))  
            
            pod = C.active_object
            podName = 'Pod'
            C.active_object.name = podName
            hole = self.buildHoleSolid()
            self.makeHole(pod, hole, 'Hole Solid')
            pod.select_set(True)
            self.setMaterial(pod, self.makeMaterial('Red',(0.5,0,0,0.95),(1,1,1)))
            return pod
        
        def makeMaterial(self, name, diffuse, specular):
            mat = bpy.data.materials.new(name)
            mat.diffuse_color = diffuse
            mat.specular_color = specular
            mat.specular_intensity = 0.5
            return mat
        
        def setMaterial(self, ob, mat):
            me = ob.data
            me.materials.append(mat)
            
        def makeHole(self, main, hole, holeMakerName):
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
            O.mesh.primitive_uv_sphere_add(ring_count = 256, segments = 256, location = (self.location[0],self.location[1],self.location[2] + 0.14), scale = (0.28,0.28,0.28))
            holeSolid = C.active_object
            holeMakerName = 'Hole Solid'
            C.active_object.name = holeMakerName 
            return holeSolid   
        
        def buildMarble(self):
            O.mesh.primitive_uv_sphere_add(location = (self.location[0],self.location[1],self.location[2] + 0.01))
            marble = C.active_object
            marble.scale = (self.r,self.r,self.r)
            marbleName = 'Marble'
            C.active_object.name = marbleName
            self.setMaterial(marble, self.makeMaterial('Blue',(0,0,0.5,1),(1,1,1)))
            return marble
        
            
        def updateMarbleFrame(self):
            
            if self.marbleOnPod:   
                m = 0.00273 #marble mass // Between: 0.004529 kg & 0.00273 kg 
                u = 0.070
                g = 9.81
                r = self.r
                
                # calculat the normal force
                C = [self.marble.location[0] - self.pod.location[0], self.marble.location[1] - self.pod.location[1],self.marble.location[2] - (self.pod.location[2]+r)]
                B = [0.0, 0.0,40-r]
                A = [self.marble.location[0] - self.pod.location[0], self.marble.location[1] - self.pod.location[1],self.marble.location[2] - (self.pod.location[2]+40.0)]
                C_dim = pow((pow(abs(C[0]),2)+pow(abs(C[1]),2))+pow(abs(C[2]),2),0.5)
                B_dim = pow((pow(abs(B[0]),2)+pow(abs(B[1]),2))+pow(abs(B[2]),2),0.5)
                A_dim = pow((pow(abs(A[0]),2)+pow(abs(A[1]),2))+pow(abs(A[2]),2),0.5)
                
                vectorForceNormal = [0.0,0.0]
                if C_dim > r/5 or C_dim < -r/5 :
                    Q = math.acos(((A_dim **2) + (B_dim **2) - (C_dim **2))/(2*A_dim*B_dim))
                    F = m*g*math.sin(Q)
                    
                    # build normal vector 2d from the marble to the center direction
                    vector = [self.pod.location[0] - self.marble.location[0], self.pod.location[1] - self.marble.location[1]]
                    vectorModule = pow((pow(abs(vector[0]),2)+pow(abs(vector[1]),2)),0.5)
                    vectorForceNormal = [vector[0]*F/(vectorModule),vector[1]*F/(vectorModule)]
                
                self.addMarbleForce([vectorForceNormal[0],vectorForceNormal[1], 0.0])
                
                
                # calculat the friction force
                frictionForce = [0.0,0.0,0.0]
                frictionForce[0] = -self.marbleForceVec[0]*u
                frictionForce[1] = -self.marbleForceVec[1]*u
                frictionForce[2] = -self.marbleForceVec[2]*u
                
                self.addMarbleForce(frictionForce)

                # apply force to marble
                vecProjection = [0.0,0.0,0.0]
                vecProjection[0] = self.marble.location[0]+(self.marbleForceVec[0]/m)
                vecProjection[1] = self.marble.location[1]+(self.marbleForceVec[1]/m)
                vecProjection[2] = self.marble.location[2]+(self.marbleForceVec[2]/m)
                
                vecSphereMarble = [vecProjection[0] - self.pod.location[0], vecProjection[1] - self.pod.location[1],vecProjection[2] - (self.pod.location[2]+40.0)]

                moduleProjection = pow((pow(abs(vecSphereMarble[0]),2)+pow(abs(vecSphereMarble[1]),2))+pow(abs(vecSphereMarble[2]),2),0.5)
                
                self.marble.location[0] = vecSphereMarble[0]*(40-r)/moduleProjection + self.pod.location[0]
                self.marble.location[1] = vecSphereMarble[1]*(40-r)/moduleProjection + self.pod.location[1]
                self.marble.location[2] = vecSphereMarble[2]*(40-r)/moduleProjection + self.pod.location[2]+(40)
                
                self.marble.keyframe_insert(data_path = 'location')
                
                vecCenterMarble= [0.0,0.0,0.0]
                vecCenterMarble[0] = self.marble.location[0]-self.pod.location[0]
                vecCenterMarble[1] = self.marble.location[1]-self.pod.location[1]
                vecCenterMarble[2] = self.marble.location[2]-self.pod.location[2]+r
                
                distance = ((vecCenterMarble[0]**2)+(vecCenterMarble[1]**2)+(vecCenterMarble[2]**2))**0.5
                
                if distance >0.021:
                    self.marbleOnPod = False
                    
                
# //////////////////////////   RUN TEST   ///////////////////////////////////////////////
      
#clearMesh()

#frames = 360
#C.scene.frame_end = frames
#speed = 0.6
#s = (-0.109338794900686 + 0.93766057537244 * speed - 1.66404133282705 * (speed ** 2) + 1.33975259843262 * (speed ** 3))/24

#mp = MarblePod()
#mp.initMove([0.0,0.0,0.0])

#for i in range(frames):
#    C.scene.frame_set(i)
##    print(i)
#    if i> 50 and i< 120:
#        mp.pod.location[0] = mp.pod.location[0] + s*(2**0.5)/2
#        mp.pod.location[1] = mp.pod.location[1] + s*(2**0.5)/2
#        
#        
#    if i> 120 and i< 170:
#        mp.pod.location[1] = mp.pod.location[1] + s
#    if i> 170 and i< 240:
#        mp.pod.location[0] = mp.pod.location[0] - s*(2**0.5)/2
#        mp.pod.location[1] = mp.pod.location[1] + s*(2**0.5)/2
#    if i> 240 and i< 340:
#        mp.pod.location[1] = mp.pod.location[1] - s
#    
#    
#    if i> 49:
#        mp.pod.keyframe_insert(data_path = 'location')
#        mp.updateMarbleFrame()

#    
#C.scene.frame_set(0)
#O.screen.animation_play()
