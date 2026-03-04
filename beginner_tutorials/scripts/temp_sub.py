#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float32

def callback(msg):
    rospy.loginfo("온도 수신: %.1f", msg.data)
    if msg.data >= 35.0:
        rospy.loginfo("경고! 온도가 높습니다!")

def listener():
    rospy.init_node('temp_sub')
    rospy.Subscriber('temp', Float32, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()