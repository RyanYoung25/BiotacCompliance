#!/usr/bin/env python
'''
This node is run in conjunction with the biotac_sensors exceutable. It will
get the pressure from the biotac sensor and correlate it with elbow joint commands
on hubo.

Author: John, Ryan
'''

import roslib; roslib.load_manifest('BiotacCompliance')
import rospy
import time
import sys
from hubomsg.msg import *
from biotac_sensors.msg import *

ID_NUM = 14
RSR_UPPER = -1.3
RSR_LOWER = 0
REP_UPPER = -1.57
REP_LOWER = 0

INCREMENT = .03
UDTHRESHOLD = 1200
LRTHRESHOLD = 1400
'''
This is a demo class. It basically when created will handle
the demo. Every time it gets a biotac_pub message it goes through
the call back. 
'''
class demo:
    

    def __init__(self):
        rospy.init_node("BiotacCompliance")
        rospy.Subscriber("biotac_pub", BioTacHand, self.update)
        self.pub = rospy.Publisher("Maestro/Control", MaestroCommand)
        
        self.REP = 0
        self.RSR = 0

        self.count = 0
        rospy.on_shutdown(self.exit)
        rospy.spin()
    
    '''
    The heart of the demo 
    '''
    def update(self, handData):
        data = handData.bt_data
        electrodes = data[0].electrode_data
        upCheck = int((electrodes[6] + electrodes[7] + electrodes[8] + electrodes[9]) / 4)
        rightCheck = int((electrodes[10] + electrodes[13] + electrodes[15]) / 3 )
        leftCheck = int((electrodes[0] + electrodes[3] + electrodes[5]) / 3)
        downCheck = int((electrodes[17] + electrodes[18]) / 2)
        self.count += 1
        if self.count == 10:

            if upCheck < UDTHRESHOLD:
                self.moveUp()
            elif downCheck < UDTHRESHOLD:
                self.moveDown()
            if leftCheck < LRTHRESHOLD:
                self.moveLeft()
            elif rightCheck < LRTHRESHOLD:
                self.moveRight()

            print "Right: " + str(rightCheck)
            print "Left: " + str(leftCheck)
            print "Up: " + str(upCheck)
            print "Down: " + str(downCheck)

            self.pub.publish("RSR REP", "position position", str(self.RSR) + " " + str(self.REP), "", ID_NUM)
            self.count = 0

    # Bend the elbow pitch
    def moveLeft(self):
        temp = self.REP - INCREMENT
        if(temp > REP_UPPER):
            self.REP = temp

    # Straighten the elbow pitch
    def moveRight(self):
        temp = self.REP + INCREMENT
        if(temp < REP_LOWER):
            self.REP = temp

    # Move the shoulder roll out
    def moveUp(self):
        temp = self.RSR - INCREMENT
        if(temp > RSR_UPPER):
            self.RSR = temp

    # Move the shoulder roll in
    def moveDown(self):
        temp = self.RSR + INCREMENT
        if(temp < RSR_LOWER):
            self.RSR = temp


    def exit(self):
        self.pub.publish("RSR REP", "position position", "0 0", "", ID_NUM)
        


    
if __name__ == '__main__':
    print "Starting the biotac elbow demo"
    demo = demo()
    
