#!/usr/bin/env python

import rospy
import sys
from std_msgs.msg import Float32MultiArray

import manageSpreadSheet
import spreadSheets

class BenchmarkResultsGrabber:

  def __init__(self,topic):
    image_sub = rospy.Subscriber(topic,Float32MultiArray,self.results_callback)
    self.buffer=[]
    self.appendable=[0,1,0,1,1,1,1,1,1,1,1,1,1,1,0]
    self.mutex=0

  def results_callback(self,data):
    newdata=[]
    for x in xrange(0, len(data.data), len(self.appendable)):
      newline=[]
      for y in xrange(len(self.appendable)):
	if self.appendable[y]==1:
	  newline.append(data.data[x+y])
      newdata.append(newline)

    if newdata:
      while self.mutex:
        rospy.sleep(0.1)
      self.mutex=1
      self.buffer+=newdata
      self.mutex=0

  def getBuffer(self):
    while self.mutex:
      rospy.sleep(0.1)
    self.mutex=1
    copy=list(self.buffer)
    self.buffer=[]
    self.mutex=0
    return copy

if __name__ == '__main__':

    rospy.init_node('cloudResults')
    resultsGrabber=BenchmarkResultsGrabber("BenchmarkResults")

    SSnames=spreadSheets.spreadSheetsNames()

    uploadOption = rospy.get_param("/upload")
    scene = rospy.get_param("/scene")
    SSname=''
    if uploadOption =="teleop":
      if scene=="basic":
        SSname=SSnames.teleopBasic
      elif scene=="turns":
        SSname=SSnames.teleopTurns
      elif scene=="heights":
        SSname=SSnames.teleopHeights

    elif uploadOption =="waypoint":
      if scene=="basic":
        SSname=SSnames.waypBasic
      elif scene=="turns":
        SSname=SSnames.waypTurns
      elif scene=="heights":
        SSname=SSnames.waypHeights

    elif uploadOption =="vision":
      if scene=="basic":
        SSname=SSnames.visionBasic
      elif scene=="turns":
        SSname=SSnames.visionTurns
      elif scene=="heights":
        SSname=SSnames.visionHeights

    if SSname =='':
       print("WARNING: Benchmark data is not being sent to the cloud.")
       sys.exit(0)

    SSmanager=manageSpreadSheet.SpreadSheetManager(SSname)

    userEmail = SSmanager.getEmail()
    sheetId = SSmanager.getSheetId(userEmail)

    ## Add new sheet or clear current
    if sheetId<0:
      sheetId=SSmanager.createNewSheet(userEmail)
      SSmanager.appendValues([[userEmail]],'Resumen')
      SSmanager.protectSheet(userEmail,sheetId)
    else:
      SSmanager.clearSheet(sheetId)

    

    ## Write headers
    values = [["Time", "PositionError", "PEx","PEy", "PEz","Rx","Ry","Rz", "Rw", "ISE", "distanceToPath","waypoint"]]

    SSmanager.writeValues(values,userEmail,1)
    cursorLine=3
    while not rospy.is_shutdown():
      rospy.sleep(10)

      buff=resultsGrabber.getBuffer()
      print(len(buff))
      SSmanager.writeValues(buff,userEmail,cursorLine)
      cursorLine+=len(buff)


