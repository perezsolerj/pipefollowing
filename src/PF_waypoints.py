#!/usr/bin/env python

from geometry_msgs.msg import TwistStamped
import rospy
import numpy as np

#import service library
from std_srvs.srv import Empty

### WAYPOINTS
## rename to waypoints in order to use them
waypointsTurns=[[-1.4,-4.5,7.5],[1.49,4.8,7.5],[7.4,2.975,7.5],[9.29,9.0,7.5],[7.15,9.68,7.5]]
waypointsHeights=[[-4.96,-15.9,6.92],[-2.16,-6.9,6.92],[-1.96,-6.3,7.5],[1.4,4.5,7.5],[1.6,5.15,6.97],[3.84,12.35,6.97],[4.07,13,6.43],[4.63,14.8,6.43],[4.85,15.43,5.9],[6.53,20.83,5.9]]
waypointsBasic=[[1.4,4.5,7.5],[-1.4,-4.5,7.5]]

#topic to command
twist_topic="/g500/velocityCommand"
#base velocity for the teleoperation (0.5 m/s) / (0.5rad/s)
baseVelocity=0.5

##create the publisher
rospy.init_node('waypointFollow')
pub = rospy.Publisher(twist_topic, TwistStamped,queue_size=1)

##wait for benchmark init service
rospy.wait_for_service('/startBench')
start=rospy.ServiceProxy('/startBench', Empty)

##wait for benchmark stop service
rospy.wait_for_service('/stopBench')
stop=rospy.ServiceProxy('/stopBench', Empty)

#where are we moving to
currentwaypoint=1

start()
while not rospy.is_shutdown() and currentwaypoint < len(waypoints):
  msg = TwistStamped()

  msg.twist.linear.x=0.0
  msg.twist.linear.y=0.0
  msg.twist.linear.z=0.0
  msg.twist.angular.z=0.0
  pub.publish(msg)
  
  rospy.sleep(0.1)

stop()
