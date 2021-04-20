import os 
import math 
import bpy 
import sys
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O
from pathlib import Path
foldername = Path(bpy.context.space_data.text.filepath)
file = os.path.join(foldername.parent.absolute(), 'tools.py')
exec(compile(open(file).read(), file, 'exec'))

# curvePath
#   -description:
#       Courbe qui peut être manipulé par la classe Car
#   -param:
#       -Object: Objet sur lequel le parcour sera centré
#       -Center: Position de centre initiale
#       -Radius: Rayon de la courbe du parcours
#       -Angle:  Angle de rotation par rapport à Object
#       -Orientation: Orientation initiale du parcours courbé
#   -return: curvePath
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


# straightPath()
#   -description:
#       Permet d'initialiser un parcours en ligne droite dans Blender
#   -param:
#       -name: Nom du parcours qui sera créé
#       -scale_x: Grandeur en x du parcours
#       -scale_y: Grandeur en y du parcours
#       -loc_x:  location en x du parcours
#       -loc_y: location en y du parcours
#   -return: straightPath
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

# turnPath()
#   -description:
#       Permet d'instancier le parcours courbé dans Blender
#   -param:
#       -name: Nom du parcours qui sera créé
#       -radius: Rayon du parcours courbé
#       -angle: Angle du parcours
#       -direction:  Direction du parcours
#       -loc_x: location en x du parcours à instancier
#       -loc_y: location en y du parcours à instancier
#   -return: path
def turnPath(name, radius, angle, direction = 'L',loc_x =0, loc_y =0):
    
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
    hole_maker.location = ((-radius) + loc_x , loc_y, 0.0)
    
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
    angle_maker.location = ((-radius) + loc_x, loc_y , 0)
    
    bpy.ops.mesh.primitive_cube_add() 
    C.active_object.name = "Hole maker2" 
    hole_maker2 = C.active_object
    hole_maker2.scale = (radius, (2*radius+0.1), 1.1)
    hole_maker2.location = (loc_x, loc_y, 0.0)
    
    makeHole(angle_maker, hole_maker2, 'Hole maker2')

    #Rotate and cut
    angle_maker.rotation_euler = (0,0,math.radians(270+angle))
    makeHole(path, angle_maker, 'Angle maker')
    
    p = curvePath(path,center,radius, math.radians(angle),0)
    
    if direction == 'R':
        p.rotate(math.radians(90))
        p.move(2*radius,0)
    
    return p
    
#  buildObstacle()
#   -description:
#       Construit un obstacle.
#   -param: NONE
#   -return:
#       [0]: lineToCarSupport
def buildObstacle():
    O.mesh.primitive_cube_add() 
    C.active_object.name = "Obstacle" 
    obs =C.active_object
    obs.dimensions = (0.075, 0.064, 0.115)
    return obs




    

