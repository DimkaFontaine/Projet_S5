import os 
import sys
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O

# clearMesh()
#   -description:
#       Supprime tous les objets instanciés dans la simulation
#   -param:
#   -return: void
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

# makeHole(main, hole, holeMakerName = '')
#   -description:
#       Fait un trou dans l'objet main avec l'objet hole
#   -param:
#       -main: L'objet qui recevera le trou
#       -hole: L'objet qui produit un trou dans l'objet main
#       -holeMakerName (Optionel): Possibilité de spécifier le nom de l'objet qui fera le trou
#   -return: void
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

# makeIntersect(main, intersect, holeMakerName = '')
#   -description:
#       Fait l'intersection entre l'objet main et l'objet intersect.
#   -param:
#       -main: L'objet qui recevera le trou
#       -hole: L'objet qui produit un trou dans l'objet main
#       -holeMakerName (Optionel): Possibilité de spécifier le nom de l'objet qui fera l'intersection
#   -return: void
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

# makeIntersect(name, diffuse, specular)
#   -description:
#       Permet de créer un nouveau matériel
#   -param:
#       -name: Nom du nouveau matériel
#       -diffuse: Propriété d'un matériel dans Blender
#       -spectacular: Propriété d'un matériel dans Blender
#   -return: Nouveau matériel
def makeMaterial(name, diffuse, specular):
                mat = bpy.data.materials.new(name)
                mat.diffuse_color = diffuse
                mat.specular_color = specular
                mat.specular_intensity = 0.5
                return mat

# setMaterial(ob, mat)
#   -description:
#       Permet d'appliquer un matériel à um objet Blender
#   -param:
#       -name: Nom du nouveau matériel
#       -diffuse: Propriété d'un matériel dans Blender
#       -spectacular: Propriété d'un matériel dans Blender
#   -return: Nouveau matériel
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)


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

def minusVec2(a,b):
    c = [0.0,0.0]
    c[0] = a[0] - b[0]
    c[1] = a[1] - b[1] 
    return c
        
def multVec3(a,b):
    c = [0.0,0.0,0.0]
    c[0] = a[0] * b[0]
    c[1] = a[1] * b[1]
    c[2] = a[2] * b[2] 
    return c

def multVec2(a,b):
    c = [0.0,0.0]
    c[0] = a[0] * b[0]
    c[1] = a[1] * b[1] 
    return c

def prodScalarVec3(a,b):
    c = multVec3(a,b)
    return c[0]+ c[1] + c[2]

def prodScalarVec2(a,b):
    c = multVec2([a[0],a[1],0.0],b)
    return c[0]+ c[1]


#location dans le monde du coin d'un cube 
def rectCornerToWorld(col):
    a =  [col.scale[0]*math.cos(col.rotation_euler[2]) - col.scale[1]*math.sin(col.rotation_euler[2]), col.scale[0]*math.sin(col.rotation_euler[2]) + col.scale[1]*math.cos(col.rotation_euler[2])]
    b =  [col.scale[0]*math.cos(col.rotation_euler[2]) - (-col.scale[1])*math.sin(col.rotation_euler[2]), col.scale[0]*math.sin(col.rotation_euler[2]) + (-col.scale[1])*math.cos(col.rotation_euler[2])]    
    c = [(-col.scale[0])*math.cos(col.rotation_euler[2]) - (-col.scale[1])*math.sin(col.rotation_euler[2]), (-col.scale[0])*math.sin(col.rotation_euler[2]) + (-col.scale[1])*math.cos(col.rotation_euler[2])]
    d =  [(-col.scale[0])*math.cos(col.rotation_euler[2]) - col.scale[1]*math.sin(col.rotation_euler[2]), (-col.scale[0])*math.sin(col.rotation_euler[2]) + col.scale[1]*math.cos(col.rotation_euler[2])]

    a = [col.location[0]+a[0], col.location[1]+a[1]]
    b = [col.location[0]+b[0], col.location[1]+b[1]]
    c = [col.location[0]+c[0], col.location[1]+c[1]]
    d = [col.location[0]+d[0], col.location[1]+d[1]]
    
    return a,b,c,d


# regarde si un point est dans le rectangle
def pointInRect(p, rect):
    
    a,b,c,d = rectCornerToWorld(rect)
    
    vecAB = minusVec2(b,a)
    vecAD = minusVec2(d,a)
    vecAP = minusVec2(p,a)
    
    vecCB = minusVec2(b,c)
    vecCD = minusVec2(d,c)
    vecCP = minusVec2(p,c)
    
    return prodScalarVec2(vecCP,vecCB) > 0 and prodScalarVec2(vecCP,vecCD) > 0 and prodScalarVec2(vecAP,vecAB) > 0 and prodScalarVec2(vecAP,vecAD) > 0
    

# regarde si un point est dans le cercle de la courbe
def pointInCurve(p, curve, demiLargeur = 0.009):
    
    c = curve.centerWorld
    r = curve.radius
    a0 = curve.orientation
    a1 =  a0 + curve.angle
    
    vec = minusVec2(p,c)
    distance = distance2(vec)
    angle = math.atan(abs(vec[1])/abs(vec[0]))

    if vec[0] < 0:
        if vec[1] < 0:
            angle = angle + math.pi
        else:
            angle = math.pi - angle
    else:
         if vec[1] < 0:
            angle = (2*math.pi) - angle
    
    return distance < r+demiLargeur and distance > r-demiLargeur and angle > a0 and angle < a1




def distance3(vector):
    return pow((pow(abs(vector[0]),2)+pow(abs(vector[1]),2))+pow(abs(vector[2]),2),0.5)

def distance2(vector):
    return pow((pow(abs(vector[0]),2)+pow(abs(vector[1]),2)),0.5)


# ray cast pour les capteurs
# param: col = objet à detecter
def rayCast2dObstacle(posInit, orientation, col, maxDistance = 1.0, precision = 0.1):

    minDistancePossible = distance3(col.location) - distance3([col.scale[0],col.scale[1],0.0])
    rayStep = [0.0, 0.0, 0.0]
    for i in range(3):
        rayStep[i] = orientation[i]*precision
    ray = [0.0, 0.0, 0.0]
    
    while distance3(ray) < maxDistance :
        ray = addVec3(ray,rayStep)
        pos  = addVec3(posInit,ray)
        if distance3(pos) > minDistancePossible :
            if pointInRect(pos,col):
                return [True, pos]
    return [False, [0.0,0.0,0.0]]
