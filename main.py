import os 
import sys
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O
import tools as tools
from pathlib import Path
import path as path

os.system("cls") # clean console
print("Clean objecs...")
tools.clearMesh()      # destroy all mesh object && reset animation too the start

print("Load files...")

foldername = Path(bpy.context.space_data.text.filepath)
file1 = os.path.join(foldername.parent.absolute(), 'path.py')
exec(compile(open(file1).read(), file1, 'exec'))
file2 = os.path.join(foldername.parent.absolute(), 'Car.py')
exec(compile(open(file2).read(), file2, 'exec'))

print("Build paths...")
lines = []
curves = []
obs = []

lines, curves, obs = path.straightLineForwardTest()
#lines, curves, obs = straightLineBackwardTest()
#lines, curves, obs = straightLineForwardWithObstacleTest()
#lines, curves, obs = straightLineForwardWithObstacleInMiddleTest()
#lines, curves, obs = leftCurveTest()
#lines, curves, obs = rightCurveTest()
#lines, curves, obs = tightLeftCurveTest()
#lines, curves, obs = tightRightCurveTest()



print("Build car...")
car = Car(orientation = math.pi/2, rightLines = lines, curveLines = curves,obstacles = obs)


print("Compute car behavior...")
    
frames = 800
C.scene.frame_end = frames

car.setSpeed(50)

for i in range(frames): 
    
    C.scene.frame_set(i)  
    car.update1in24frame() 
    r = car.detectLigne()     
    
    if r[2]:
        car.setWheels(90)
    if r[0]:
        car.setWheels(0)
    if r[4]:
        car.setWheels(180)
    if r[1]:
        car.setWheels(70)
    if r[3]:
        car.setWheels(110)
    
    if not r[0] and not r[1] and not r[2] and not r[3] and not r[4] :
        car.setSpeed(0)
        
    if car.getSonar() < 0.1 :
        car.setSpeed(0)
        


C.scene.frame_set(0) 
print("Ready")
