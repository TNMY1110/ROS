#!/bin/bash
# Gazebo 시뮬레이션 환경 사전 점검 스크립트
# 학생 VM에서 실행하여 2주차 Gazebo 수업 가능 여부를 확인합니다.
#
# 사용법: bash check_gazebo_ready.sh

# set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
BOLD='\033[1m'

pass=0
warn=0
fail=0

print_header() {
    echo ""
    echo -e "${BOLD}=== $1 ===${NC}"
}

result_pass() {
    echo -e "  ${GREEN}[PASS]${NC} $1"
    ((pass++))
}

result_warn() {
    echo -e "  ${YELLOW}[WARN]${NC} $1"
    ((warn++))
}

result_fail() {
    echo -e "  ${RED}[FAIL]${NC} $1"
    ((fail++))
}

echo ""
echo -e "${BOLD}Gazebo 시뮬레이션 환경 사전 점검${NC}"
echo "======================================"

# --- CPU ---
print_header "CPU"

cpu_model=$(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)
cpu_cores=$(nproc)
echo "  모델: $cpu_model"
echo "  코어 수: ${cpu_cores}개"

if [ "$cpu_cores" -ge 8 ]; then
    result_pass "CPU 코어 충분 (${cpu_cores}코어)"
elif [ "$cpu_cores" -ge 4 ]; then
    result_warn "CPU 코어 최소 수준 (${cpu_cores}코어, 권장 8코어 이상)"
else
    result_fail "CPU 코어 부족 (${cpu_cores}코어, 최소 4코어 필요)"
fi

# --- RAM ---
print_header "RAM"

ram_total_kb=$(grep MemTotal /proc/meminfo | awk '{print $2}')
ram_total_gb=$((ram_total_kb / 1024 / 1024))
ram_available_kb=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
ram_available_gb=$((ram_available_kb / 1024 / 1024))
echo "  전체: ${ram_total_gb}GB"
echo "  사용 가능: ${ram_available_gb}GB"

if [ "$ram_total_gb" -ge 8 ]; then
    result_pass "RAM 충분 (${ram_total_gb}GB)"
elif [ "$ram_total_gb" -ge 4 ]; then
    result_warn "RAM 최소 수준 (${ram_total_gb}GB, 권장 8GB 이상)"
else
    result_fail "RAM 부족 (${ram_total_gb}GB, 최소 4GB 필요)"
fi

# --- GPU / 3D 가속 ---
print_header "GPU / 3D 가속"

if command -v glxinfo &> /dev/null; then
    renderer=$(glxinfo 2>/dev/null | grep "OpenGL renderer" | cut -d: -f2 | xargs)
    echo "  렌더러: $renderer"

    if echo "$renderer" | grep -qi "llvmpipe\|softpipe\|swrast"; then
        result_fail "소프트웨어 렌더링 감지 — VMware 3D 가속을 활성화하세요"
        echo "         VMware: VM 설정 → Display → Accelerate 3D graphics 체크"
    else
        result_pass "하드웨어 3D 가속 활성화됨"
    fi
else
    result_warn "glxinfo 미설치 — 3D 가속 확인 불가"
    echo "         설치: sudo apt install mesa-utils"
fi

# --- 디스크 ---
print_header "디스크"

disk_available=$(df -BG /home 2>/dev/null | tail -1 | awk '{print $4}' | tr -d 'G')
echo "  /home 여유 공간: ${disk_available}GB"

if [ "$disk_available" -ge 40 ]; then
    result_pass "디스크 여유 충분 (${disk_available}GB)"
elif [ "$disk_available" -ge 20 ]; then
    result_warn "디스크 여유 최소 수준 (${disk_available}GB, 권장 40GB 이상)"
else
    result_fail "디스크 여유 부족 (${disk_available}GB, 최소 20GB 필요)"
fi

# --- ROS 설치 ---
print_header "ROS"

if [ -n "$ROS_DISTRO" ]; then
    echo "  ROS 배포판: $ROS_DISTRO"
    result_pass "ROS 환경 로드됨 ($ROS_DISTRO)"
else
    result_fail "ROS 환경 미로드 — source /opt/ros/noetic/setup.bash 필요"
fi

# --- Gazebo 설치 ---
print_header "Gazebo"

if command -v gazebo &> /dev/null; then
    gz_version=$(gazebo --version 2>/dev/null | head -1)
    echo "  버전: $gz_version"
    result_pass "Gazebo 설치됨"
else
    result_fail "Gazebo 미설치 — sudo apt install ros-noetic-gazebo-ros-pkgs"
fi

if dpkg -l | grep -q "ros-noetic-gazebo-ros"; then
    result_pass "gazebo_ros 패키지 설치됨"
else
    result_fail "gazebo_ros 미설치 — sudo apt install ros-noetic-gazebo-ros-pkgs"
fi

# --- TurtleBot3 패키지 ---
print_header "TurtleBot3 (선택)"

if dpkg -l 2>/dev/null | grep -q "ros-noetic-turtlebot3-gazebo"; then
    result_pass "turtlebot3_gazebo 설치됨"
else
    result_warn "turtlebot3_gazebo 미설치"
    echo "         설치: sudo apt install ros-noetic-turtlebot3-gazebo"
fi

if dpkg -l 2>/dev/null | grep -q "ros-noetic-turtlebot3-simulations"; then
    result_pass "turtlebot3_simulations 설치됨"
else
    result_warn "turtlebot3_simulations 미설치"
    echo "         설치: sudo apt install ros-noetic-turtlebot3-simulations"
fi

# --- Gazebo 실행 테스트 ---
print_header "Gazebo 실행 테스트"

if command -v gzserver &> /dev/null; then
    echo "  gzserver를 5초간 실행합니다..."
    timeout 5 gzserver --verbose /usr/share/gazebo-11/worlds/empty.world > /tmp/gz_test.log 2>&1 &
    gz_pid=$!
    sleep 3

    if kill -0 $gz_pid 2>/dev/null; then
        result_pass "gzserver 정상 실행됨"
        kill $gz_pid 2>/dev/null || true
        wait $gz_pid 2>/dev/null || true
    else
        result_fail "gzserver 실행 실패 — /tmp/gz_test.log 확인"
    fi
else
    result_warn "gzserver를 찾을 수 없어 실행 테스트 생략"
fi

# --- 결과 요약 ---
echo ""
echo "======================================"
echo -e "${BOLD}점검 결과 요약${NC}"
echo "======================================"
echo -e "  ${GREEN}PASS${NC}: ${pass}개"
echo -e "  ${YELLOW}WARN${NC}: ${warn}개"
echo -e "  ${RED}FAIL${NC}: ${fail}개"
echo ""

if [ "$fail" -eq 0 ] && [ "$warn" -eq 0 ]; then
    echo -e "  ${GREEN}${BOLD}Gazebo 시뮬레이션 준비 완료!${NC}"
elif [ "$fail" -eq 0 ]; then
    echo -e "  ${YELLOW}${BOLD}대부분 준비됨 — WARN 항목을 확인하세요.${NC}"
else
    echo -e "  ${RED}${BOLD}FAIL 항목을 해결해야 Gazebo 수업 진행이 가능합니다.${NC}"
fi
echo ""