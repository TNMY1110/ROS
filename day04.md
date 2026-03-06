# action
## 환경설정
### package.xml
```bash
<build_depend>actionlib</build_depend>
<build_depend>actionlib_msgs</build_depend>
<exec_depend>actionlib</exec_depend>
<exec_depend>actionlib_msgs</exec_depend>
```
### CMakeLists.txt
```bash
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
  actionlib              # 추가
  actionlib_msgs         # 추가
)

add_action_files(
  FILES
  Timer.action
)

generate_messages(
  DEPENDENCIES
  std_msgs
  actionlib_msgs         # 추가
)

catkin_package(
  CATKIN_DEPENDS actionlib_msgs   # 추가
)
```
### action 디렉토리 생성
```bash
cd ~/catkin_ws/beginner_tutorials
mkdir action
```

## actionlib
ROS 서비스에서 사용자는 두 노드 간의 요청/응답 상호작용을 구현하지만 응답에 너무 오랜 시간이 걸리거나 서버가 요청 작업을 완료하지 않은 경우 완료될 때까지 기다려야 하므로 기다리는 동안 메인 애플리케이션이 블록 상태가 된다. 또한 원격 프로세스의 실행을 모니터링 하고 싶다면 호출 클라이언트를 추가로 구현해야 한다. 이런 경우 actionlib을 사용해 애플리케이션을 구현하면 간편하다
actionlib은 실행 중인 요청을 선점하고 예상대로 요청이 제 시간에 완료되지 않은 경우 다른 요청을 보낼 수 있는 통신 방법이다.

## 액션 파일 요소
- Goal: 액션 서버가 수행해야 하는 목표(예: 10초 카운트 해)
- Feedback: 콜백 함수 내에서 현재 작업의 진행상황을 알려주는 것(예: 현재 5초까지 셈)
- Result: 목표를 달성했음을 나타내는 것(예: 카운트 완료)

## 취소 매커니즘
- cancel_goal() 함수를 사용해 작업 중단 가능
- is_preempt_requested()로 감지

## 실습
### Timer.action
[Timer.action](beginner_tutorials/action/Timer.action)
[timer_server.py](beginner_tutorials/scripts/timer_server.py)
[timer_client.py](beginner_tutorials/scripts/timer_client.py)