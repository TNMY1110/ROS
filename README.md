# ROS development
ubuntu 20.04.6
ROS neotic

# ROS install
source list
```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
```

```bash
sudo apt install curl
```

```bash
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
```

```bash
sudo apt update
```

```bash
sudo apt install ros-noetic-desktop-full
```

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