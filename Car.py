import os 
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



class Car:
    def __init__(self, location = (0.0,0.0), orientation = 0.0, obstacles = [], lines = []):
        self.body = self.buildCar();
        self.body.location[0] = location[0]
        self.body.location[1] = location[1]
        self.body.location[2] = 0.0675
        self.body.rotation_euler[2] = orientation
        self.obstacles = obstacles
        self.lines = lines

    def buildCar(self):
        
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
        
        
        def makeSoundSensor():
            O.mesh.primitive_cylinder_add()  
            sensor = C.active_object
            sensor.delta_scale = (0.01, 0.01, 0.0075)
            sensor.rotation_euler = (0.0,math.pi/2,0.0)
            return sensor
        
        def makeLineSensor():
            O.mesh.primitive_cube_add()   
            sensor = C.active_object
            sensor.delta_scale = (0.005, 0.0025, 0.0025)
            return sensor
        
        
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
        
        # Build distance sensor
        soundSensorR = makeSoundSensor()
        C.active_object.name = "SoundSensorR" 
        soundSensorR.location = (0.1275,-0.0175,0.02)
        soundSensorL = makeSoundSensor()
        C.active_object.name = "SoundSensorL" 
        soundSensorL.location = (0.1275,0.0175,0.02)
        
        # Build line detector structure
        bpy.ops.mesh.primitive_cube_add() 
        C.active_object.name = "LineToCarSupport" 
        lineToCarSupport =C.active_object
        lineToCarSupport.delta_scale = (0.0075, 0.03, 0.0015)
        lineToCarSupport.location = (0.1275,0.0,-0.0435)
        
        bpy.ops.mesh.primitive_cube_add() 
        C.active_object.name = "LineSupport" 
        lineSupport =C.active_object
        lineSupport.delta_scale = (0.015, 0.05125, 0.0015)
        lineSupport.location = (0.15,0.0,-0.0435)
        
        # Build line sensors
        # 0 to 4 => left to right
        lineSensor4 = makeLineSensor()
        C.active_object.name = "LineSensor4" 
        lineSensor4.location = (0.1575,-0.0375 ,-0.0475)
        lineSensor3 = makeLineSensor()
        C.active_object.name = "LineSensor3" 
        lineSensor3.location = (0.1575,-0.01875 ,-0.0475)
        lineSensor2 = makeLineSensor()
        C.active_object.name = "LineSensor2" 
        lineSensor2.location = (0.1575,0.0 ,-0.0475)
        lineSensor1 = makeLineSensor()
        C.active_object.name = "LineSensor1" 
        lineSensor1.location = (0.1575,0.01875 ,-0.0475)
        lineSensor0 = makeLineSensor()
        C.active_object.name = "LineSensor0" 
        lineSensor0.location = (0.1575,0.0375 ,-0.0475)
        
        
        # Parent object
        O.object.empty_add(type='SPHERE')
        C.active_object.name = "Car" 
        car = C.active_object
        
        O.object.select_all(action='DESELECT')
        
        for o in bpy.context.scene.objects: 
            if o.type == 'MESH': 
                o.select_set(True) 
        car.select_set(True)
        
        O.object.parent_set(type='OBJECT')
        O.object.select_all(action='DESELECT')
        
        
        
        return car
    
    
    


    # sensorFeedback(sensor, orientation, colliders)
    #   -description:
    #       simulate the behavior of a sensor A.K.A Usful and usable raycasting
    #   -param:
    #       sensor: 
    #           mesh object that simulates the sensor
    #       orientation: 
    #           the orientation that we want it to detect, in relation to the world (independent of the orientation of the sensor)
    #       colliders:
    #           list of objects that we want to be able to detect
    #   -return:
    #       [0] : name of the object detected (None if not detected)
    #       [1] : distance of the object detected (-1 if not detected)
    #
    def sensorFeedback(self,sensor, orientation, colliders): 
        
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

        def distance3(vector):
            return pow((pow(vector[0],2)+pow(vector[1],2))+pow(vector[2],2),0.5)
        
        for col in colliders: 
            loc = [sensor.location[0]-col.location[0],sensor.location[1]-col.location[1],sensor.location[2]-col.location[2]]
            results = col.ray_cast(loc, orientation) 
            if results[0]: 
                q = addVec3(col.location,results[1])
                v = minusVec3(q,sensor.location)
                d = distance3(v)
                return [col.name,d] 
        return [None,-1.0]
    
    
    def getSonar(self):
        s1 = bpy.context.scene.objects['SoundSensorR']
#        self.sensorFeedback()
        return
    
    

print("Reset") 

clearMesh()      # destroy all mesh object && reset animation too the start
os.system("cls") # clean console 
print("Start") 

car = Car(orientation = math.pi/2)



print("End")
