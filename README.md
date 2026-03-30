# COMP219 Group 4's Warehouse Autonomous Navigation Project

Welcome to the COMP219 Group 4 - robotics project repository! This package contains the Gazebo simulation environment and the ROS 2 mobile robot model for our autonomous navigation system.

## 🛠️ Prerequisites
- **OS:** Ubuntu 22.04 / 24.04 (Native or WSL2)
- **ROS 2:** Humble / Iron / Jazzy (Ensure your distribution is fully installed)
- **Gazebo:** Modern Gazebo (Fortress or Harmonic) + `ros_gz_sim` bridge packages

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
colcon build --packages-select comp219_warehouse
```

**4. Source the environment**
```bash
source install/setup.bash
```
*(💡 Tip: Add `source ~/project_ws/install/setup.bash` to your `~/.bashrc` file so you don't have to run this manually every time you open a new terminal.)*

## 🎮 Running the Simulation

To launch the warehouse world, the robot state publisher, and the ROS-GZ bridges all at once, run:

```bash
ros2 launch comp219_warehouse warehouse_launch.py
```

**⚠️ WSL11 Users Troubleshooting:** If Gazebo crashes, freezes, or opens with a black/white screen without colors, press `Ctrl+C` to kill the process and force software rendering by running:
```bash
export LIBGL_ALWAYS_SOFTWARE=1
ros2 launch comp219_warehouse warehouse_launch.py
```

## 🤝 Git Collaboration Workflow

To keep our codebase clean and prevent merge conflicts, please follow this workflow when adding new features (e.g., SLAM, Nav2, or the LLM node):

**1. Always pull the latest changes before starting work:**
```bash
git checkout main
git pull origin main
```

**2. Create a new branch for your feature:**
```bash
# Example: git checkout -b feature/slam-mapping
git checkout -b feature/your-feature-name
```

**3. Work on your code, build, and test it locally.**

**4. Commit your changes with a clear message:**
```bash
git add .
git commit -m "Add short description of what you did"
```

**5. Push your branch to GitHub:**
```bash
git push origin feature/your-feature-name
```

**6. Create a Pull Request (PR):**
Go to the GitHub repository page and click **"Compare & pull request"**. The team will review the code and merge it into `main` together.
