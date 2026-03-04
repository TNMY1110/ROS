#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose

def callback(msg):
    poseX = msg.x
    poseY = msg.y
    rospy.loginfo("위치 수신: x = %f, y = %f", poseX, poseY)
    if poseX <= 1.0 or poseX >= 10.0 or poseY <= 1.0 or poseY >= 10.0 :
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