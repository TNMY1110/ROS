# ROS development
- ubuntu 20.04.6
- ROS neotic

# ROS install
source list
1. ROS 저장소(Repository) 추가하기
```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```
2. 보안 키(Key) 등록하기
```bash
sudo apt install curl
```
```bash
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
```
3. 패키지 리스트 업데이트
```bash
sudo apt update
```
4. ROS 패키지
```bash
sudo apt install ros-noetic-desktop-full
```
5. 환경 설정
```bash
source /opt/ros/noetic/setup.bash
```
```bash
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
```
```bash
source ~/.bashrc
```

# Installing and Configuring Your ROS Environment
1. Managing Your Environment
```bash
printenv | grep ROS
```
```bash
source /opt/ros/neotic/setup.bash
```

2. Create a ROS Workspace
```bash
mkdir -p ~/catkin_ws/src
```
```bash
cd ~/catkin_ws/
```
```bash
catkin_make
```

# turtle/pose 관찰
- x: 거북이의 X 좌표. 윈도우 창 기준 우측으로 이동하면 값이 증가
- y: 거북이의 Y 좌표. 윈도우 창 기준 상단으로 이동하면 값이 증가
- theta: 거북이의 방향 (라디안). 좌회전하면 값이 증가, 우회전하면 감소
- linear_velocity: 현재 속도. 방향키 상하를 누르면 2.0이 된다
- angular_velocity: 현재 회전 속도. 방향키 좌를 누르면 2.0, 우를 누르면 -2.0이 된다

# 토픽 목록 확인
```bash
$ rostopic list
```
* /rosout
* /rosout_agg
* /turtle1/cmd_vel
* /turtle1/color_sensor
* /turtle1/pose

# 토픽 메시지 타입 확인
```bash
$ rostopic type /turtle1/cmd_vel
```
geometry_msgs/Twist

```bash
$ rostopic type /turtle1/color_sensor
```
turtlesim/Color

```bash
$ rostopic type /turtle1/pose
```
turtlesim/Pose

# 토픽 메시지 구조 확인
```bash
$ rosmsg show geometry_msgs/Twist
```
* geometry_msgs/Vector3 linear
  - float64 x
  - float64 y
  - float64 z
* geometry_msgs/Vector3 angular
  - float64 x
  - float64 y
  - float64 z

```bash
$ rosmsg show turtlesim/Color
```
- uint8 r 
- uint8 g 
- uint8 b 

```bash
$ rosmsg show turtlesim/Pose
```
- float32 x
- float32 y
- float32 theta
- float32 linear_velocity
- float32 angular_velocity

## turtlesim 토픽 정리
### /turtle1/cmd_vel (geometry_msgs/Twist)
1. linear
- x: 직진 속도 (앞/뒤)
- y: 좌/우 이동 (사용 안 함)
- z: 상/하 이동 (사용 안 함)

2. angular
- x: Roll (사용 안 함)
- y: Pitch (사용 안 함)
- z: 회전 속도 (좌/우 회전)


### /turtle1/color_sensor (turtlesim/Color)
- r: 빨강(0~255)
- g: 초록(0~255)
- b: 파랑(0~255)

### /turtle1/pose (turtlesim/Pose)
- x: 거북이의 X 좌표
- y: 거북이의 Y 좌표
- theta: 방향
- linear_velocity: 현재 직진 속도
- angular_velocity: 현재 회전 속도

# 정사각형 그리기
- '[linear.x, linear.y, linear.z]' '[angular.x, angular.y, angular.z]'

## 명령어
```bash
$ rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[2.0, 0.0, 0.0]' '[0.0, 0.0, 0.0]'
```
publishing and latching message for 3.0 seconds
```bash
$ rostopic pub -1 /turtle1/cmd_vel geometry_msgs/Twist -- '[0.0, 0.0, 0.0]' '[0.0, 0.0, 1.56]'
```
publishing and latching message for 3.0 seconds

- 총 4회 반복

## 결과
1. x축으로 2 이동
2. 좌로 약 90도 회전
3. y축으로 2 이동
4. 좌로 약 90도 회전
5. x축으로 -2 이동
6. 좌로 약 90도 회전
7. y축으로 -2 이동

# turtlesim 2개 동시 실행
## 명령어
### 터미널 1
```bash
$ roscore
```

### 터미널 2
```bash
$ rosrun turtlesim turtlesim_node
```

### 터미널 3
```bash
$ rosrun turtlesim turtlesim_node __name:=my_turtle
```

### 터미널 4
```bash
$ rostopic info /turtle1/cmd_vel
```
### 결과
- 두 거북이가 동시에 움직임.

```bash
$ rostopic info /turtle1/cmd_vel
```

Type: geometry_msgs/Twist

Publishers: 
 * /teleop_turtle (http://ubuntu:38617/)

Subscribers: 
 * /my_turtle (http://ubuntu:35419/)
 * /turtlesim (http://ubuntu:43123/)
 