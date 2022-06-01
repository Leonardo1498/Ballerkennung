import math
#import Robo
import ballerkennung as be
import torwarterkennung

#laufe zum Ball
def run_to_ball():
    radius, distance_to_center = be.ballerkennung()
    while(radius is None):
        # turn right
        print("...turning right")
        radius,distance_to_center = be.ballerkennung()
    #negativer Wert --> rechts von Mitte des Bildes
    #positiver Wert --> links von Mitte des Bildes
    while(abs(distance_to_center)>15):
        if(distance_to_center<0):
            # turn left
            print("...turning left")
            radius, distance_to_center = be.ballerkennung()
        else:
            # turn right
            print("...turning right")
            radius, distance_to_center = be.ballerkennung()
    print(distance_to_center)
#drehe Richtung Tor
    #go forward until distance < ?
def turn_to_goal():
    pass
#schuss
def shoot():
    pass

if __name__ == '__main__':
    run_to_ball()