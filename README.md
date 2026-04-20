SETUP & RUNNING INSTRUCTIONS
=============================

1. Create a workspace (if you haven't already)

    mkdir -p ~/project_ws/src
    cd ~/project_ws/src


2. Extract the project files

   - Locate the downloaded project ZIP file in your Downloads folder
   - Right-click the ZIP file and select "Extract All..." (Windows) or double-click to unzip (Mac)
   - The unzipped folder should now be in your Downloads folder


3. Copy the project files into WSL

   In your open WSL terminal, run the following command to copy the unzipped
   project folder from your Windows Downloads folder into your workspace src directory:

    cp -r /mnt/c/Users/<YourWindowsUsername>/Downloads/<unzipped-folder-name>/. ~/project_ws/src/

   Replace <YourWindowsUsername> with your actual Windows username (e.g. John)
   and <unzipped-folder-name> with the name of the extracted folder.


4. Build the workspace

    cd ~/project_ws
    source/opt/ros/jazzy/setup.bash
    colcon build


5. Add your Mistral API Key

   The AI agent requires a Mistral API key to function. You need to create a .env
   file in the project workspace containing your key.

   First, create the .env file:

    touch ~/project_ws/.env

   Then open it with gedit:

    gedit ~/project_ws/.env

   In the gedit window that opens, paste the following and replace the placeholder
   with your actual Mistral API key, then save and close the file:

    MISTRAL_API_KEY=your_mistral_api_key_here

   For example, if your key is abc123xyz, the file should contain:

    MISTRAL_API_KEY=abc123xyz


6. Running the Project

   --- Terminal 1: Start the Gazebo Simulation & Robot ---
    cd ~/project_ws
    source install/setup.bash
    ros2 launch project_description gazebo.launch.py


   --- Terminal 2: Start Nav2 and RViz ---
   cd ~/project_ws
   source install/setup.bash
   ros2 launch project_nav2_bringup nav2.launch.py


   --- Terminal 3: AI AGENT ---
   cd ~/project_ws
   source venv/bin/activate
   source install/setup.bash
   ros2 run ros2_basic_agent warehouse_agent

   --- Terminal 4: ---
   Once the agent is running, you can type the following sample commands:
    go to room 1
    go to room 2
    go to room 3
    go to room 4
    go to service desk
    go to charging station
    get a PC
    get a monitor
    get a laptop
    get accessories
    get cables
   
   Example command:
   ros2 topic pub --once /prompt std_msgs/msg/String "{data: 'Go to the room with the monitors'}"
