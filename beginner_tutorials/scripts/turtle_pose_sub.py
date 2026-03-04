#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose

def callback(msg):
    rospy.loginfo("위치 수신: x = %f, y = %f", msg.x, msg.y)
    if msg.x <= 1.0 or msg.x >= 10.0 or msg.y <= 1.0 or msg.y >= 10.0 :
        rospy.loginfo("경고! 벽이 가깝습니다!")

def listener():
    rospy.init_node('turtle_pose')
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

    # topic list = /turtle1/pose
    # topic type = turtlesim/Pose
    # msg 
    # float32 x
    # float32 y
    # float32 theta
    # float32 linear_velocity
    # float32 angular_velocity