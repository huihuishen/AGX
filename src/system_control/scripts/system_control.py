#!/usr/bin/env python
#coding=utf-8
import rospy
import roslaunch
from std_msgs.msg import Int8

global power_on
global  power_off
power_on=1
power_off=0
global power_cmd
# 0-掉电,1-上电
power_cmd=0
global  power_state
# 0-未上电,1-已上电
power_state=0
#上下电控制字和状态字


#模式切换控制字和状态字
global mode_cmd
global mode_state




def power_cmd_callback(data):    
    global power_on
    global  power_off
    global  power_cmd
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if data.data==1:        
        power_cmd=power_on
    else:
        power_cmd=power_off

def mode_cmd_callback(data):

    print "更换模式"

def  power_on_fuction():
    print "上电"


def  power_off_fuction():
    print "下电"


def slam_nav_task_start():
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/controlstation/Multi-Robots-CCS/install/share/bit_task_desc/launch/bit_qt.launch"])
    launch.start()
    rospy.loginfo("started")

#订阅接收上位机话题信息
def system_control():
    rospy.Subscriber("/power_cmd", Int8, power_cmd_callback)
    rospy.Subscriber("/mode_cmd",Int8,mode_cmd_callback)


if __name__ == '__main__':
    
    rospy.init_node('en_Mapping', anonymous=True)
    system_control()
    while not rospy.is_shutdown(): 
        # print power_cmd
        if (power_cmd and (not power_state)):
            power_on_fuction()
            power_state=1
        elif (not power_cmd and (power_state)):
            power_off_fuction()
            power_state=0

    
            