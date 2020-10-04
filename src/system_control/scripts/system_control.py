#!/usr/bin/env python
#coding=utf-8
import rospy
import roslaunch
from std_msgs.msg import Int8
from geometry_msgs.msg import Twist
from v_detection.srv import  v_detection_task

    


#机器人移动的数据来源切换
global change_source
change_source=0
# 0-表示使用上位机发布的话题指令
# 1-表示使用机器人自身进行决策所得到的话题指令

global slam_used
slam_used=0
# 0-表示自主导航未开启
# 1表示导航已开启

#控制字和状态字 类
class cmd_state:
	def __init__(self):
		self.cmd= 0
		self.state= 0

#导航AGX订阅
def hand_control_callback(data):
    global change_source
    if  change_source==0:
        hand_control(data)
    elif change_source==1:
         pass



 #手动或手柄遥控数据解析
def hand_control(data):
    # cmd_vel=data.x
    # 将上位机控制站发布的手柄或者面板按键发布的移动话题转析，才能进入话题转速度指令解析包
    # ，而自主导航时，则选择直通，即自主导航的输出即为ROS cmd_vel，

    vel_pub.publish
    print "转析话题"
    pass

#模式控制
def mode_change_fuction():
    global change_source
    if mode.cmd== 0 or mode.cmd==1 or mode.cmd==2 or mode.cmd==3 or mode.cmd==5 or mode.cmd==6:#只要不是自主导航，其他模式下都可以手动遥控
        if change_source==1:
            slam_nav_task(0)
        elif mode.cmd==5:
            #调取视觉识别程序
            v_detection_task("door")
        print "识别门"
        change_source=0        
    elif mode.cmd==4:
        slam_nav_task(1)
        change_source=1

        

    print  mode.cmd
    mode.state=mode.cmd


#自主任务的启停
def slam_nav_task(switch):
    global slam_used
    if switch==1:
        launch.start()
        rospy.loginfo("started")
        # type(launch)
    elif switch==0:
        launch.shutdown()
        slam_used=0
 
def mode_cmd_callback(data):
    mode.cmd=data.data
     
#订阅接收上位机话题信息
rospy.Subscriber("/mode_cmd",Int8,mode_cmd_callback)
rospy.Subscriber("/turtle1/cmd_vel",Int8,hand_control_callback)#订阅手柄或者面板按键发出的运动控制话题#话题名称为robot.xml中的<twist_topic>
vel_pub = rospy.Publisher('cmd_vel',Twist, queue_size = 10)
v_detection_task = rospy.ServiceProxy('v_detection_task',  v_detection_task)

move_Twist=Twist()#转析上位机控制站话题的消息


if __name__ == '__main__':

    rospy.init_node('system_control', anonymous=True)

    
    mode=cmd_state()

    while not rospy.is_shutdown(): 


        # 控制模式切换
        if mode.cmd !=0:
            if mode.cmd != mode.state:
            #保证相同的指令每次切换时只响应一次
                mode_change_fuction()


            #任务launch启动项
            # 当slam_used==0时代表当前未运行slam自主任务，同时通过
        if slam_used==0:
            uuid = roslaunch.rlutil.get_or_generate_uuid(None, True)
            roslaunch.configure_logging(uuid)
            launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/controlstation/AGX/src/slam_task/launch/turtle.launch"])
            slam_used=1
        # elif slam_used==-1:
        #     uuid = roslaunch.rlutil.get_or_generate_uuid(None, True)
        #     roslaunch.configure_logging(uuid)
        #     launch = roslaunch.parent.ROSLaunchParent(uuid, ["/home/controlstation/AGX/src/slam_task/launch/turtle.launch"])
        #     slam_used=1
        #     print "新建"
