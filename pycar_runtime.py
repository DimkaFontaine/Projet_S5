from SunFounder_Line_Follower import Line_Follower
from SunFounder_Ultrasonic_Avoidance import Ultrasonic_Avoidance
from picar import front_wheels
from picar import back_wheels
import time
import picar
import sys


picar.setup()


fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')
lf = Line_Follower.Line_Follower()
ua = Ultrasonic_Avoidance.Ultrasonic_Avoidance(20)
lineCalib = 70

class Car:
    def __init__(self):
        self.currentState = 0
        self.nextState = 0
        self.setSpeed(50)

    
    def getSonar(self):
        distance = ua.get_distance()
        if distance != -1:
            return distance / 100.0
        else:
            return 3.0


    def detectLigne(self):
        colors = lf.read_analog()
        digital = [0,0,0,0,0]
        for i in range(5):
            if colors[i] < lineCalib:
                digital[i] = 1
        return digital

    def setSpeed(self,speed):
        if speed > 0:
            bw.forward()
            bw.speed = speed
        elif speed <0:
            bw.backward()
            bw.speed = abs(speed)
        else:
            bw.stop()

    def setWheels(self,angle):
        fw.turn(angle)
        
    def panicTurn(self, direction):
        time.sleep(1.2)
        self.setSpeed(0)
        self.setWheels(0 if direction == 'R' else 180)
        time.sleep(1.5)
        self.setSpeed(-40)
        time.sleep(1.8)
        self.setSpeed(0)
        time.sleep(0.5)
            
    def getAround(self):
        self.setWheels(90)
        self.setSpeed(0)
        time.sleep(5)
        self.setSpeed(-40)
        dist = self.getSonar()
        while dist < 0.3 or dist > 1 :
            time.sleep(0.1)
            dist = self.getSonar()
            print(dist)
        self.setSpeed(0)
        self.setWheels(60)
        time.sleep(1)
        self.setSpeed(50)
        time.sleep(2.8)
        self.setWheels(105)
        time.sleep(2.3)
        self.setWheels(135)
        time.sleep(0.5)

    
    #state 
    #0 = straight no line
    #1 = tightL
    #2 = Left
    #3 = stright
    #4 = right
    #5 = tightR
    #6 = panic Left backward
    #7 = panic Left forward
    #8 = panic Right backward
    #9 = panic Right forward
    #10 = obstacle
    #-1 = stop all
    def followLine(self):
        lineDetector = self.detectLigne()
        distance = self.getSonar()
        
            
        if distance < 0.1 :
            self.nextState = 10
        elif self.currentState == 10:
            self.nextState = 11
        elif self.currentState == 6:
            self.nextState = 7
        elif self.currentState == 8:
            self.nextState = 9    
        elif lineDetector == [1,1,1,1,1] or lineDetector == [0,1,1,1,1] or lineDetector == [1,1,1,1,0]:
            self.nextState = -1
        elif lineDetector == [0,0,0,0,0] and self.currentState == 0:
            self.nextState = 0
        elif lineDetector == [0,0,0,0,0] and self.currentState == 1:
            self.nextState = 6
        elif lineDetector == [0,0,0,0,0] and self.currentState == 5:
            self.nextState = 8
        elif lineDetector[0] == 1 and self.currentState !=7:
            self.nextState = 1
        elif lineDetector[1] == 1:
            self.nextState = 2
        elif lineDetector[4] == 1 and self.currentState !=9: 
            self.nextState = 5
        elif lineDetector[3] == 1:
            self.nextState = 4
        elif lineDetector[2] == 1:
            self.nextState = 3
                    
        self.currentState = self.nextState

        if self.currentState == -1:
            self.setSpeed(0)
            print("Fin du trajet")
            time.sleep(60)
        elif self.currentState == 1:
            self.setWheels(0)
            time.sleep(0.2)
            self.setSpeed(30)
        elif self.currentState == 2:
            self.setWheels(70)
            time.sleep(0.2)
            self.setSpeed(40)
        elif self.currentState == 3:
            self.setWheels(90)
            time.sleep(0.2)
            self.setSpeed(50)
        elif self.currentState == 4:
            self.setWheels(110)
            time.sleep(0.2)
            self.setSpeed(40)
        elif self.currentState == 5:
            self.setWheels(180)
            time.sleep(0.2)
            self.setSpeed(30)
        elif self.currentState == 6:
            self.panicTurn('L')
        elif self.currentState == 7:
            self.setWheels(80)
            self.setSpeed(30)
        elif self.currentState == 8:
            self.panicTurn('R')
        elif self.currentState == 9:
            self.setWheels(100)
            self.setSpeed(30)
        elif self.currentState == 10:
            print("Obstacle!") 
            self.getAround()
        elif self.currentState == 11: 
            self.setSpeed(50)
            self.setWheels(180)

        return True

def carLogic():
    car = Car()
    while True:
        car.followLine()


def startCalib():
    while True:
        print(lf.read_analog())
        time.sleep(1)

def stop():
    bw.stop()
    fw.turn_straight()

def startTest():
    fw.turn_straight()
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    
    carLogic()
    
    stop()
    

    
if __name__ == '__main__':
    try:
        print(sys.argv)
        if len(sys.argv) > 1:
            if sys.argv[1] == 'calib':
                startCalib()
       	    elif sys.argv[1] == 'delay':
                print("Start in: 30s")
                time.sleep(30)
                startTest()
            else:
                print(sys.argv)
        else:
            startTest()
    except KeyboardInterrupt:
        stop()


