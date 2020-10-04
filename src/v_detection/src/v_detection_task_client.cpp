#include "ros/ros.h"
#include "v_detection/v_detection_task.h"
#include <cstdlib>
 
int main(int argc, char **argv)
{
  ros::init(argc, argv, "v_detection_task_client");
  if (argc != 1)
  {
    ROS_INFO("usage: v_detection_task_cliernt ");
    return 1;
  }
 
  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<v_detection::v_detection_task>("v_detection_task");
  v_detection::v_detection_task srv;
  srv.request.target   = atoll(argv[1]);

  if (client.call(srv))
  {
    // ROS_INFO("TargetPose: %s",  string   srv.request.target);
  }
  else
  {
    // ROS_ERROR("Failed to call service v_detection_task");
    return 1;
  }
 
  return 0;
}
