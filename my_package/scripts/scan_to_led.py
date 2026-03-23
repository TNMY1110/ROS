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


    def filter_data(self, data_list):
        # 0.0(오류값)이나 inf를 제외하고 유효한 데이터만 필터링
        # 유효한 데이터가 하나도 없으면 10.0(안전거리)을 반환
        valid_data = [x for x in data_list if x > 0.12] # LDS 최소 측정거리 0.12m
        return valid_data if valid_data else [10.0]    

    def scan_callback(self, scan):
        if len(scan.ranges) < 360:
            return

        # 현 코드상으로 필요없긴 한데 일단 방향 범위 나눠놓음
        front_range = scan.ranges[0:45] + scan.ranges[315:360]
        left_range  = scan.ranges[45:135]
        back_range  = scan.ranges[135:225]
        right_range = scan.ranges[225:315]

        self.regions = {
            'front':  min(self.filter_data(front_range)),
            'left':   min(self.filter_data(left_range)),
            'back':   min(self.filter_data(back_range)),
            'right':  min(self.filter_data(right_range)),
            } 

    def cmd_callback(self, twist):
        # 방향에 상관없이 가장 가까운 거리에 따라 불이 들어옴
        if self.regions and min(self.regions.values()) < DIST_THRESHOLD:
            self.publish_led('red')

        # 전진 중이라면 초록
        elif twist.linear.x > 0:
            self.publish_led('green')

        # 후진 중이라면 파랑
        elif twist.linear.x < 0:
            self.publish_led('blue')

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