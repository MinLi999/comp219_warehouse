# COMP219 Group 4's Warehouse Autonomous Navigation Project

Welcome to the COMP219 Group 4 - robotics project repository! This package contains the Gazebo simulation environment and the ROS 2 mobile robot model for our autonomous navigation system.

## 🛠️ Prerequisites
- **OS:** Ubuntu 24.04 (Native or WSL2)
- **ROS 2:** Jazzy 
- **Gazebo:** Harmonic (Modern Gazebo)

## 🚀 Setup & Installation (For Team Members)

**1. Create a workspace (if you haven't already)**
```bash
mkdir -p ~/project_ws/src
cd ~/project_ws/src
```

**2. Clone this repository**
```bash
git clone https://github.com/minli999/comp219_warehouse.git
```

**3. Build the workspace**
```bash
cd ~/project_ws
source /opt/ros/jazzy/setup.bash
colcon build
```

**4. Runing the Project**

**Terminal 1: Start the Gazebo Simulation & Robot**

```bash
cd ~/project_ws
source install/setup.bash
ros2 launch project_description gazebo.launch.py
```

**Terminal 2: Start Nav2 and RViz**

```bash
cd ~/project_ws
source install/setup.bash
ros2 launch project_nav2_bringup nav2.launch.py
```

**📍 How to Navigate**
Look at the RViz window.

Click the "Nav2 Goal" button at the top toolbar.

Click anywhere on the map to send the robot to that location. Watch it automatically plan the path and avoid obstacles!

**⚠️ WSL11 Users Troubleshooting:** If Gazebo crashes, freezes, or opens with a black/white screen without colors, press `Ctrl+C` to kill the process and force software rendering by running:
```bash
wsl --shutdown
```

## 🤝 Git Collaboration Workflow

Before you start making changes, always pull the latest updates:

```bash
cd ~/project_ws/src
git pull origin main
When you add new features, commit and push:
```
When you add new features, commit and push:

```bash
cd ~/project_ws/src
git add .
git commit -m "Describe what you changed"
git push origin main
```