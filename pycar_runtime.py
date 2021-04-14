
from picar import front_wheels
from picar import back_wheels
import time
import picar


picar.setup()

fw = front_wheels.Front_Wheels(db='config')
bw = back_wheels.Back_Wheels(db='config')

def stop():
    bw.stop()
    fw.turn_straight()


def startTest():
    print("Start in:")
    print("3...")
    time.sleep(1)
    print("2...")
    time.sleep(1)
    print("1...")
    time.sleep(1)
    
    fw.turn_straight()
    fw.turn(0)
    bw.forward()
    bw.speed = 100
    time.sleep(4)
    stop()
    

    
if __name__ == '__main__':
    try:
        startTest()
    except KeyboardInterrupt:
        stop()

