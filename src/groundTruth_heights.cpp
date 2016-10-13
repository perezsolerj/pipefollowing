#include "ros/ros.h"
#include "nav_msgs/Path.h"
#include <geometry_msgs/PoseStamped.h>

int main (int argc, char **argv){

  ros::init(argc, argv, "GTPublisher");
  ros::NodeHandle n;

  ros::Publisher path_pub = n.advertise<nav_msgs::Path>("path", 1000);
  ros::Publisher pose_pub = n.advertise<geometry_msgs::PoseStamped>("position", 1000);

  ros::Rate loop_rate(10);
  while (ros::ok()){
    nav_msgs::Path msg;
    geometry_msgs::PoseStamped poseMsg;

    msg.poses.resize(10);	
    msg.poses[0].pose.position.x = -4.96; 
    msg.poses[0].pose.position.y = -15.9; 
    msg.poses[0].pose.position.z = 6.92;

    msg.poses[1].pose.position.x = -2.16; 
    msg.poses[1].pose.position.y = -6.9; 
    msg.poses[1].pose.position.z = 6.92;

    msg.poses[2].pose.position.x = -1.96; 
    msg.poses[2].pose.position.y = -6.3; 
    msg.poses[2].pose.position.z = 7.5;

    msg.poses[3].pose.position.x = 1.4; 
    msg.poses[3].pose.position.y = 4.5; 
    msg.poses[3].pose.position.z = 7.5;

    msg.poses[4].pose.position.x = 1.6; 
    msg.poses[4].pose.position.y = 5.15; 
    msg.poses[4].pose.position.z = 6.97;

    msg.poses[5].pose.position.x = 3.84; 
    msg.poses[5].pose.position.y = 12.35; 
    msg.poses[5].pose.position.z = 6.97;

    msg.poses[6].pose.position.x = 4.07; 
    msg.poses[6].pose.position.y = 13; 
    msg.poses[6].pose.position.z = 6.43;

    msg.poses[7].pose.position.x = 4.63; 
    msg.poses[7].pose.position.y = 14.8; 
    msg.poses[7].pose.position.z = 6.43;

    msg.poses[8].pose.position.x = 4.85; 
    msg.poses[8].pose.position.y = 15.43; 
    msg.poses[8].pose.position.z = 5.9;

    msg.poses[9].pose.position.x = 6.53; 
    msg.poses[9].pose.position.y = 20.83; 
    msg.poses[9].pose.position.z = 5.9;

    poseMsg.pose.position.x =20.83;
    poseMsg.pose.position.y =6.53;
    poseMsg.pose.position.z =-5.9;

    pose_pub.publish(poseMsg);
    path_pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
  }
  return 0;
}
