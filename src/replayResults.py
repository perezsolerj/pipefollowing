#!/usr/bin/env python

import rospy
import sys
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped

import manageSpreadSheet
import spreadSheets

class PositionGrabber:

  def __init__(self,topic):
    sub = rospy.Subscriber(topic,PoseStamped,self.callback)
    self.position=[]
    self.valid=-1

  def callback(self,data):
    self.position=[data.pose.position.x,data.pose.position.y,data.pose.position.z]
    self.valid=1

  def getPosition(self):
    return self.position


if __name__ == '__main__':

    if len(sys.argv) != 4 and len(sys.argv) != 5:
      print("usage: rosrun pipefollowing replayResults.py {teleop | waypoint | vision} {basic | turns | heights} {EMAIL} [rate]")
      sys.exit(0)

    uploadOption=sys.argv[1]
    scene=sys.argv[2]

    SSnames=spreadSheets.spreadSheetsNames()
    SSname=''
    if uploadOption =="teleop":
      if scene=="basic":
        SSname=SSnames.teleopBasic
      elif scene=="turns":
        SSname=SSnames.teleopTurns
      elif scene=="heights":
        SSname=SSnames.teleopHeights
      else:
	print("Wrong scene name: valid names are basic turns heights")
	sys.exit(0)

    elif uploadOption =="waypoint":
      if scene=="basic":
        SSname=SSnames.waypBasic
      elif scene=="turns":
        SSname=SSnames.waypTurns
      elif scene=="heights":
        SSname=SSnames.waypHeights
      else:
	print("Wrong scene name: valid names are basic turns heights")
	sys.exit(0)

    elif uploadOption =="vision":
      if scene=="basic":
        SSname=SSnames.visionBasic
      elif scene=="turns":
        SSname=SSnames.visionTurns
      elif scene=="heights":
        SSname=SSnames.visionHeights
      else:
	print("Wrong scene name: valid names are basic turns heights")
	sys.exit(0)

    else:
      print("Wrong method: valid methods are teleop waypoint vision")
      sys.exit(0)

    rospy.init_node('replayResults')
    topic="/dataNavigator"
    pub = rospy.Publisher(topic, Odometry,queue_size=1)
    positionGrabber=PositionGrabber('/position')



    user=sys.argv[3]
    rate=1.0
    if len(sys.argv)==5:
      rate=float(sys.argv[4])
 

    if SSname =='':
       print("WARNING: Benchmark data is not being sent to the cloud.")
       sys.exit(0)

    SSmanager=manageSpreadSheet.SpreadSheetManager(SSname)

    ##userEmail = SSmanager.getEmail()
    sheetId = SSmanager.getSheetId(user)

    ## Check if user sheet exists.
    if sheetId<0:
      print("Requested sheet does not exist.")
      sys.exit(0)

    data=SSmanager.readSheet(user)
    lastTick=0
    for i in xrange(2,len(data)):
      msg = Odometry()

      while positionGrabber.valid==-1:
	rospy.sleep(0.1)
      position=positionGrabber.getPosition()

      time=float(data[i][0].replace(u',','.'))
      #print(type(time))
      ##print(data[i])
      msg.pose.pose.position.x=float(data[i][3].replace(u',','.'))+position[1]
      msg.pose.pose.position.y=float(data[i][2].replace(u',','.'))+position[0]
      msg.pose.pose.position.z=-float(data[i][4].replace(u',','.'))-position[2]

      ##print(msg.pose.pose.position.x,msg.pose.pose.position.y,msg.pose.pose.position.z)

      msg.pose.pose.orientation.x=float(data[i][5].replace(u',','.'))
      msg.pose.pose.orientation.y=float(data[i][6].replace(u',','.'))
      msg.pose.pose.orientation.z=float(data[i][7].replace(u',','.'))
      msg.pose.pose.orientation.w=float(data[i][8].replace(u',','.'))
      
      pub.publish(msg)
      rospy.sleep((time-lastTick)/rate)
      lastTick=time	
      

