#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import String

# ===== 파라미터 =====
DIST_THRESHOLD = 0.3   # 벽까지 이 거리 이내면 "가깝다"고 판단 (m)

class LedController:
    def __init__(self):
        rospy.init_node('led_controller')
        self.led_pub = rospy.Publisher('/led_color', String, queue_size=1)
        self.cmd_sub = rospy.Subscriber('/cmd_vel', Twist, self.cmd_callback)
        self.scan_sub = rospy.Subscriber('/scan', LaserScan, self.scan_callback)
        self.regions = {}
        self.rate = rospy.Rate(10)

    def scan_callback(self, scan):
        self.regions = {
            'right':       min(min(scan.ranges[0:72]),   10), # 영역 5개로 나눔, 10은 최솟값
            'front_right': min(min(scan.ranges[72:144]), 10),
            'front':       min(min(scan.ranges[144:216]), 10),
            'front_left':  min(min(scan.ranges[216:288]), 10),
            'left':        min(min(scan.ranges[288:360]), 10),
        }

    def cmd_callback(self, twist):
        # 근접 상태가 아닐 때만 이동 방향으로 판단
        if self.regions and min(self.regions.values()) < DIST_THRESHOLD:
            self.publish_led('red')
        elif twist.linear.x > 0:
            self.publish_led('blue')
        elif twist.linear.x < 0:
            self.publish_led('green')

    def publish_led(self, color):
        msg = String()
        msg.data = color
        self.led_pub.publish(msg)
        rospy.loginfo("LED 색상: %s", color)

    def run(self):
        rospy.loginfo("LED Controller 시작")
        rospy.spin()

if __name__ == '__main__':
    try:
        lc = LedController()
        lc.run()
    except rospy.ROSInterruptException:
        pass