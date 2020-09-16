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

#机器人移动的数据来源切换
global change_source
change_source=0

global slam_used
slam_used=0

#控制字和状态字 类
class cmd_state:
	def __init__(self):
		self.cmd= 0
		self.state= 0

def power_cmd_callback(data):    
    global power_on
    global  power_off
    global  power_cmd
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    if data.data==1:        
        power_cmd=power_on
    else:
        power_cmd=power_off

#上下电控制电源板通信控制函数
def  power_fuction(cmd):
    if  cmd==1:
        print "上电"
    if  cmd==0:
        print "下电"

def mode_cmd_callback(data):
    mode.cmd=data.data
            # if data.data==1:
            #     mode.cmd=1
            # elif data.data==2:
            #     mode.cmd=2
            # elif data.data==3:
            #     # launch.shutdown()
            #     mode.cmd=3
            # elif data.data==4:
            #     # launch.shutdown()
            #     mode.cmd=4
            # elif data.data==5:
            #     # launch.shutdown()
            #     mode.cmd=5
            # elif data.data==6:
            #     # launch.shutdown()
            #     mode.cmd=6

    # print "更换模式"

#SLAM_AGX订阅
def hand_control_callback(data):
    global change_source
    if  change_source==0:
        hand_control(data)
    elif change_source==1:
         pass
 #手动或手柄遥控数据解析
def hand_control(data):
    # cmd_vel=data.x
    print "解析手动遥控指令"
    pass

#模式控制
def mode_change_fuction():
    global change_source
    if mode.cmd== 0 or mode.cmd==1 or mode.cmd==2 or mode.cmd==3 or mode.cmd==5 or mode.cmd==6:#只要不是自主导航，其他模式下都可以手动遥控
        if change_source==1:
            slam_nav_task(0)
        change_source=0        
    elif mode.cmd==4:
        slam_nav_task(1)
        change_source=1
    print  mode.cmd

#自主任务的启停
def slam_nav_task(switch):
    global slam_used
    if switch==1:
        launch.start()
        rospy.loginfo("started")
        type(launch)
    elif switch==0:
        launch.shutdown()
        slam_used=-1
 
     
#订阅接收上位机话题信息
def subscrib_topic():
    rospy.Subscriber("/power_cmd", Int8, power_cmd_callback)
    rospy.Subscriber("/mode_cmd",Int8,mode_cmd_callback)
    rospy.Subscriber("/turtle1/cmd_vel",Int8,hand_control_callback)#订阅手柄解算发出的话题


if __name__ == '__main__':

    rospy.init_node('system_control', anonymous=True)
    subscrib_topic()
    mode=cmd_state()
    while not rospy.is_shutdown(): 
            #任务launch启动项
        if slam_used==0:
            uuid = roslaunch.rlutil.get_or_generate_uuid(None, True)
            roslaunch.configure_logging(uuid)
            launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/controlstation/AGX/src/slam_task/launch/turtle.launch"])
            slam_used=1
        elif slam_used==-1:
            uuid = roslaunch.rlutil.get_or_generate_uuid(None, True)
            roslaunch.configure_logging(uuid)
            launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/controlstation/AGX/src/slam_task/launch/turtle.launch"])
            slam_used=1
            print "新建"
            #新建
        # 上下电状态控制和切换
        if (power_cmd and (not power_state)):
            power_fuction(1)
            power_state=1
        elif (not power_cmd and (power_state)):
            power_fuction(0)
            power_state=0

        # 控制模式切换
        if mode.cmd !=0:
            if mode.cmd != mode.state:
            #保证相同的指令每次切换时只响应一次
                mode_change_fuction()
                mode.state=mode.cmd
    
        

        