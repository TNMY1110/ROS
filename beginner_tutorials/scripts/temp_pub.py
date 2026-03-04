#!/usr/bin/env python3
import rospy
import random
from std_msgs.msg import Float32

def temperature():
    pub = rospy.Publisher('temp', Float32, queue_size=10)
    rospy.init_node('temp_pub')
    rate = rospy.Rate(1)  # 1Hz = 1초에 1번

    while not rospy.is_shutdown():
        ranTemp = random.uniform(20.0, 40.0)
        rospy.loginfo("발행: %.1f", ranTemp)
        pub.publish(ranTemp)
        rate.sleep()

if __name__ == '__main__':
    try:
        temperature()

    except rospy.ROSInterruptException:
        pass
