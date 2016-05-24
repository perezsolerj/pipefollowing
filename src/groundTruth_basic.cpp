#include "ros/ros.h"
#include "nav_msgs/Path.h"

int main (int argc, char **argv){

  ros::init(argc, argv, "GTPublisher");
  ros::NodeHandle n;

  ros::Publisher path_pub = n.advertise<nav_msgs::Path>("path", 1000);

  ros::Rate loop_rate(10);
  while (ros::ok()){
    nav_msgs::Path msg;


    msg.poses.resize(2);	
    msg.poses[0].pose.position.x = 1.4; 
    msg.poses[0].pose.position.y = 4.5; 
    msg.poses[0].pose.position.z = 7.5;

    msg.poses[1].pose.position.x = -1.4; 
    msg.poses[1].pose.position.y = -4.5; 
    msg.poses[1].pose.position.z = 7.5;


    path_pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
  }
  return 0;
}
