
#include "ros/ros.h"
#include "v_detection/v_detection_task.h"
 
bool detection(v_detection::v_detection_task::Request &req,
         v_detection::v_detection_task::Response &res)
{
  //运行视觉程序
//   ROS_INFO("request: x=%ld, y=%ld", (long int)req.a, (long int)req.b);

  ROS_INFO("Start v_detection!");

  return true;
}
 
int main(int argc, char **argv)
{
  ros::init(argc, argv, "v_detection_task_server");
  ros::NodeHandle n;
 
  ros::ServiceServer service = n.advertiseService("v_detection_task", detection);
  ROS_INFO("Ready to add target.");
  ros::spin();
  
  return 0;
}