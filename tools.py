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
