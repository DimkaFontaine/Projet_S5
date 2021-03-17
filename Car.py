import os 
import sys
import math 
import bpy 
from bpy import context as C 
from bpy import data as D 
from bpy import ops as O
from pathlib import Path
foldername = Path(bpy.context.space_data.text.filepath)
file = os.path.join(foldername.parent.absolute(), 'marblePod.py')
exec(compile(open(file).read(), file, 'exec'))
file = os.path.join(foldername.parent.absolute(), 'tools.py')
exec(compile(open(file).read(), file, 'exec'))
file = os.path.join(foldername.parent.absolute(), 'path.py')
exec(compile(open(file).read(), file, 'exec'))


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



def pointInRect(p, rect):
    
    a,b,c,d = rectCornerToWorld(rect)
    
    vecAB = minusVec2(b,a)
    vecAD = minusVec2(d,a)
    vecAP = minusVec2(p,a)
    
    vecCB = minusVec2(b,c)
    vecCD = minusVec2(d,c)
    vecCP = minusVec2(p,c)
    
    return prodScalarVec2(vecCP,vecCB) > 0 and prodScalarVec2(vecCP,vecCD) > 0 and prodScalarVec2(vecAP,vecAB) > 0 and prodScalarVec2(vecAP,vecAD) > 0
    

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

def rayCast2dObstacle(posInit, orientation, col, maxDistance = 3.0, precision = 0.001):

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



class Car:


    # INIT
    def __init__(self, location = (0.0,0.0), orientation = 0.0, obstacles = [], rightLines = [], curveLines = []):
        self.body = self.buildCar();
        self.body.location[0] = location[0]
        self.body.location[1] = location[1]
        self.body.location[2] = 0.0675
        self.body.rotation_euler[2] = orientation
        self.obstacles = obstacles
        self.rightLines = rightLines
        self.curveLines = curveLines
        self.speed = 0.0
        self.turn = 0.0
        self.t = 1.0
        self.currentState = 0
        self.nextState = 0

    # MODELISATION
    def buildCar(self):
        
        def makePoll():
            O.mesh.primitive_cylinder_add()  
            poll = C.active_object
            poll.scale = (0.01, 0.01, 0.06)
            poll.rotation_euler = (math.pi/2,0.0,0.0)
            return poll
        
        def makeWheel():
            O.mesh.primitive_cylinder_add()  
            wheel = C.active_object
            wheel.scale = (0.0325, 0.0325, 0.0125)
            wheel.rotation_euler = (math.pi/2,0.0,0.0)
            return wheel
        
        
        def makeSoundSensor():
            O.mesh.primitive_cylinder_add()  
            sensor = C.active_object
            sensor.scale = (0.01, 0.01, 0.0075)
            sensor.rotation_euler = (0.0,math.pi/2,0.0)
            return sensor
        
        def makeLineSensor():
            O.mesh.primitive_cube_add()   
            sensor = C.active_object
            sensor.scale = (0.005, 0.0025, 0.0025)
            return sensor
        
        O.object.select_all(action='DESELECT')
        
        # Build main body
        bpy.ops.mesh.primitive_cube_add() 
        C.active_object.name = "Body" 
        body =C.active_object
        body.scale = (0.12, 0.045, 0.045)
        
        # Build holes for the wheels
        bpy.ops.mesh.primitive_cylinder_add() 
        C.active_object.name = "Hole maker" 
        hole_maker =C.active_object
        hole_maker.scale = (0.05, 0.05, 0.02)
        hole_maker.rotation_euler = (math.pi/2,0.0,0.0)
        hole_maker.location = (0.08,0.045,-0.035)
        makeHole(body, hole_maker)
        hole_maker.location = (0.08,-0.045,-0.035)
        makeHole(body, hole_maker)
        hole_maker.location = (-0.08,0.045,-0.035)
        makeHole(body, hole_maker)
        hole_maker.location = (-0.08,-0.045,-0.035)
        makeHole(body, hole_maker, 'Hole maker')
        
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
        lineToCarSupport.scale = (0.0075, 0.03, 0.0015)
        lineToCarSupport.location = (0.1275,0.0,-0.0435)
        
        bpy.ops.mesh.primitive_cube_add() 
        C.active_object.name = "LineSupport" 
        lineSupport =C.active_object
        lineSupport.scale = (0.015, 0.05125, 0.0015)
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
        car.scale = (0.0001, 0.0001, 0.0001)
        
        O.object.select_all(action='DESELECT')
        
        body.select_set(True)
        lineSensor0.select_set(True)
        lineSensor1.select_set(True)
        lineSensor2.select_set(True)
        lineSensor3.select_set(True)
        lineSensor4.select_set(True)
        lineSupport.select_set(True)
        lineToCarSupport.select_set(True)
        poll1.select_set(True)
        poll2.select_set(True)
        soundSensorR.select_set(True)
        soundSensorL.select_set(True)
        wheelFR.select_set(True)
        wheelFL.select_set(True)
        wheelBR.select_set(True)
        wheelBL.select_set(True)
        
        car.select_set(True)
        
        O.object.parent_set(type='OBJECT')
        O.object.select_all(action='DESELECT')
        
        return car
    

    # Sensors ------------------------------------------------------
    
    def sensorFeedback(self, sensorPosition, orientation, colliders): 
        for col in colliders: 
            results = rayCast2dObstacle(sensorPosition, orientation, col) 
            if results[0]: 
                if False:
                    print(results)
                    bpy.ops.mesh.primitive_cube_add()
                    obs2 =C.active_object
                    obs2.scale = (0.01, 0.01, 1.0)
                    obs2.location = results[1]
                v = minusVec3(results[1],sensorPosition)
                d = distance3(v)
                return [col.name,d] 
        return [None,50.0]
    
    
    def localToWorldLocation(self, carPart):
        currentRad = self.body.rotation_euler[2]
        localX =  carPart.location[0]*math.cos(currentRad) - carPart.location[1]*math.sin(currentRad)
        localY =  carPart.location[0]*math.sin(currentRad) + carPart.location[1]*math.cos(currentRad)
        pos = [0.0,0.0,0.0]
        pos[0] = self.body.location[0] + localX
        pos[1] = self.body.location[1] + localY
        pos[2] = self.body.location[2] + carPart.location[2]
        return pos

        
    
    
    def getSonar(self):
        
        soundR = self.localToWorldLocation(C.scene.objects['SoundSensorR'])
        soundL = self.localToWorldLocation(C.scene.objects['SoundSensorL'])
        currentAngle = self.body.rotation_euler[2] - (math.pi/12)
        angles = []
        results = []
        
        for i in range(5):
            angles.append(currentAngle + (i*(math.pi/24)))
        
        for rad in angles:
            results.append(self.sensorFeedback(soundR, [math.cos(rad), math.sin(rad), 0.0], self.obstacles))
            results.append(self.sensorFeedback(soundL, [math.cos(rad), math.sin(rad), 0.0], self.obstacles))
        
        def sortFunc(a):
            return a[1]
        
        results.sort(key = sortFunc)
        return results[0][1]
    
    
    def detectLigne(self):
        s0 = self.localToWorldLocation(C.scene.objects['LineSensor0'])
        s1 = self.localToWorldLocation(C.scene.objects['LineSensor1'])
        s2 = self.localToWorldLocation(C.scene.objects['LineSensor2'])
        s3 = self.localToWorldLocation(C.scene.objects['LineSensor3'])
        s4 = self.localToWorldLocation(C.scene.objects['LineSensor4'])
        
        s = [s0,s1,s2,s3,s4]
        results = [False,False,False,False,False,]
        for i in range(5):
            for l in range(len(self.rightLines)):
                if pointInRect(s[i], self.rightLines[l]) :
                    results[i] = True
                    
            for k in range(len(self.curveLines)):
                if pointInCurve(s[i], self.curveLines[k]) :
                    results[i] = True
        return results
        
  
    
    
    
    
    # Movement ------------------------------------------------------------
    
    def accelerate(self, percent):
        percent = 100 - percent
        if percent > 16:
            gamma = self.acceleration(percent)
            self.speed = gamma*self.t/24.0
            print(gamma)
            self.t+=1.0
        else:
            self.speed =0.0
        

    def acceleration(self,speed, t=1):
        d_V = -0.0109338794900686 + 0.093766057537244 * speed - 0.166404133282705 * (speed ** 2) + 0.133975259843262 * (speed ** 3)
        return d_V * (t ** 2)
    
    def setSpeed(self, percent):
#        self.speed = self.acceleration(percent)
        
        #Temp 
        self.speed = 0.0028 * percent - 0.0277
        if percent <16:
            self.speed = 0.0
            
    def setWheels(self, deg):
        self.turn = (-(deg - 90)* math.pi)/360
        
    def update1in24frame(self):
        self.updateRotate()
        self.updateLocation()
        self.setKeyframe()
        
    def setKeyframe(self):
        self.body.keyframe_insert(data_path = 'location')
        self.body.keyframe_insert(data_path = 'rotation_euler')
        
    def updateLocation(self):
        x = self.speed*math.cos(self.body.rotation_euler[2])/24
        y = self.speed*math.sin(self.body.rotation_euler[2])/24
        self.body.location[0] = self.body.location[0] + x
        self.body.location[1] = self.body.location[1] + y
        
    def updateRotate(self):
        if self.speed > 0.0:
            deltaWheels = 0.145
            nbTic = (deltaWheels/(self.speed/24))
            deltaTurn = self.turn/nbTic
            self.body.rotation_euler[2] = self.body.rotation_euler[2]+deltaTurn
            
         def getAround(self):
        print("get around")
        
    
    #state 0 = begin
    #      1 = tightL
    def followLine(self):
        lineDetector = self.detectLigne();
        
        if lineDetector == [0,0,0,0,0] and self.currentState == 0:
            self.nextState = 3 
        elif lineDetector == [0,0,0,0,0] and self.currentState == 1:
            self.nextState = 6
        elif lineDetector == [0,0,0,0,0] and self.currentState == 5:
            nextState = 7
        elif lineDetector[0] == 1:
            self.nextState = 1
        elif lineDetector[1] == 1:
            self.nextState = 2
        elif lineDetector[4] == 1: 
            self.nextState = 5
        elif lineDetector[3] == 1: 
            self.nextState = 4
        elif lineDetector[2] == 1:
            self.nextState = 3
        else:
            self.nextState = self.currentState
        
        self.currentState = self.nextState

        if self.currentState == 1:
            self.setWheels(0)
        elif self.currentState == 2:
            self.setWheels(45)
        elif self.currentState == 3:
            self.setWheels(90)
        elif self.currentState == 4:
            self.setWheels(135)
        elif self.currentState == 5:
            self.setWheels(180)
        elif self.currentState == 6:
            print("panic gauche")
        elif self.currentState == 7:
            print("panic droite")

#/////////////////////////////    Fonction Test   //////////////////////////////////////////////////////////


def testModelisation():
    car = Car()
    marblePod = MarblePod(location = (0.085, 0, 0.1125))
    
def testDetectionObstacle(case):
    bpy.ops.mesh.primitive_cube_add() 
    C.active_object.name = "Obs" 
    obs =C.active_object
    obs.dimensions = (0.2, 0.2, 0.3)
    obs.location = (0.0,1.8,0.0)
    obs.rotation_euler[2] = math.pi/4

    bpy.ops.mesh.primitive_cube_add() 
    C.active_object.name = "Obs1" 
    obs1 = C.active_object
    obs1.dimensions = (0.2, 0.2, 0.3)
    obs1.location = (1.0,1.0,0.0)

    if case == 0:
        car = Car(orientation = math.pi*(1.0/4.0), obstacles = [obs,obs1])
    elif case == 1:
        car = Car(orientation = math.pi*(12.0/20.0), obstacles = [obs,obs1])
    else:
        car = Car(obstacles = [obs,obs1])
    
    car.body.location[0] = 0.5
    car.body.location[1] = 0.5

    val = car.getSonar()
    print(val)


def testSpeedAndTurn():

    car = Car(orientation = math.pi*(1.0/2.0))
    
    car.setSpeed(40)
    
    frames = 250 
    for i in range(frames): 
    
        C.scene.frame_set(i) 
        car.update1in24frame() 
        if i == 40:
            car.setWheels(0)
        if i == 140:
            car.setWheels(90)
            car.setSpeed(80)
        if i == 180:
            car.setSpeed(40)
            car.setWheels(180)
        if i == 240:
            car.setSpeed(0)
    # Play
    O.screen.animation_play() 

def testLines(case):
    
    bpy.ops.mesh.primitive_plane_add() 
    C.active_object.name = "Ligne" 
    obs1 = C.active_object
    obs1.scale = (0.009, 0.5, 1.0)
    obs1.location = (0.00,1.0,0.0)
    obs1.rotation_euler[2] = math.pi/20
    
    car = Car(orientation = math.pi*(1.0/2.0), rightLines = [obs1])
    car.setSpeed(50)
    
    frames = 250 
    for i in range(frames): 
    
        C.scene.frame_set(i) 
        car.update1in24frame() 
        r = car.detectLigne()
        if r[case]:
            car.setSpeed(0)
        
    # Play
    O.screen.animation_play()

def testLines2(case, straight, curve):
    car = Car(orientation = math.radians(90), rightLines = straight, curveLines = curve)
    car.setSpeed(50)
    
    frames = 500 
    for i in range(frames): 
    
        C.scene.frame_set(i) 
        car.update1in24frame() 
        r = car.detectLigne()
        if r[case]:
            car.setSpeed(0)
        
    # Play
    O.screen.animation_play()
    
    def testStateMachine():
    line = []
    line.append(straightPath("1", scale_y = 0.5,loc_y = 0.1, loc_x = -0.3))
    line[0].rotation_euler = (0,0,10)
    bpy.ops.mesh.primitive_cube_add() 
    C.active_object.name = "Obs" 
    obs =C.active_object
    obs.dimensions = (0.2, 0.2, 0.3)
    obs.location = (-0.8,1.8,0.0)
    car = Car(orientation = math.radians(90), rightLines = line, obstacles = [obs])
    
    car.setSpeed(50)
    
    frames = 300 
    for i in range(frames): 
    
        C.scene.frame_set(i) 
        car.update1in24frame() 
        
        distance= car.getSonar()
        
        if distance < 0.3:
            car.setSpeed(0)
            car.getAround()
        else:
            car.followLine()
        
    # Play
    O.screen.animation_play()


# //////////////////////////   RUN TEST   ///////////////////////////////////////////////

#print("Reset") 
#clearMesh()      # destroy all mesh object && reset animation too the start
#os.system("cls") # clean console 
#print("Start")

#testModelisation()
#testDetectionObstacle(0)
#testDetectionObstacle(1)
#testSpeedAndTurn()
#testLines(1)
#testLines(3)
testStateMachine()

#print("End")
