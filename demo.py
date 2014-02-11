#!/usr/bin/env python
'''
This node is run in conjunction with the biotac_sensors exceutable. It will
get the pressure from the biotac sensor and correlate it with elbow joint commands
on hubo.

Author: Ryan
'''

import roslib; roslib.load_manifest('BiotacCompliance')
import rospy
import time
import sys
from hubomsg.msg import *
from biotac_sensors.msg import *

ID_NUM = 14
'''
This is a demo class. It basically when created will handle
the demo. Every time it gets a biotac_pub message it goes through
the call back. 
'''
class demo:

    def __init__(self):
        self.INCREMENT = .05
        self.MAX = 1
        rospy.init_node("BioTacDemo")
        rospy.Subscriber("biotac_pub", BioTacHand, self.update)
        self.pub = rospy.Publisher("Maestro/Control", MaestroCommand)
        self.count = 0
        rospy.on_shutdown(self.exit)
        rospy.spin()
    
    '''
    The heart of the demo 
    '''
    def update(self, handData):
        data = handData.bt_data
        electrodes = data[0].electrode_data
        cd
        self.pub.publish("REP", "position", str(pos), "", ID_NUM)

    def exit(self):
        self.pub.publish("REP", "position", "0", "", ID_NUM)
        self.pub.publish("RSR", "position", "0", "", ID_NUM)
        


    
if __name__ == '__main__':
    print "Starting the biotac elbow demo"
    demo = demo()
    
