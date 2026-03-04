#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist

def turtlerun():
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('turtle_move_circle')
    rate = rospy.Rate(1)  # 1Hz = 1초에 1번
    move = Twist()
    
    while not rospy.is_shutdown():
        move.linear.x = 2.0
        move.angular.z = 1.5
        rospy.loginfo("발행: linear=%f, angular=%f", move.linear.x, move.angular.z)
        pub.publish(move)
        rate.sleep()

if __name__ == '__main__':
    try:
        turtlerun()

    except rospy.ROSInterruptException:
        pass
