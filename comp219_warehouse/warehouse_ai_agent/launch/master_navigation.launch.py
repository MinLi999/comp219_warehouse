import os
import xacro # Make sure to import this!
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Paths to your packages
    pkg_nav = get_package_share_directory('warehouse_ai_agent')
    pkg_description_share = get_package_share_directory('project_description')
    
    # Configuration paths
    nav_params_path = os.path.join(pkg_nav, 'config', 'nav2_params.yaml')
    rviz_config_path = os.path.join(pkg_nav, 'rviz', 'nav2_default_view.rviz')
    map_yaml_path = os.path.join(pkg_nav, 'maps', 'map.yaml')
    agent_config_path = os.path.join(pkg_nav, 'config', 'map_locations.yaml')

    # 2. Configuration Variables
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    workspace_src = os.path.expanduser('~/project_ws/src')

    # 3. --- ROBUST PATH DETECTION FOR URDF/XACRO ---
    # Attempt 1: Check the standard 'install' location
    xacro_file = os.path.join(
        workspace_src, 
        'comp219_warehouse-main', 
        'comp219_warehouse', 
        'project_description', 
        'urdf', 
        'rosbot.xacro'
    )

    if not os.path.exists(xacro_file):
        # Fallback for team members who might not have the -main suffix
        xacro_file = os.path.join(workspace_src, 'comp219_warehouse', 'project_description', 'urdf', 'rosbot.xacro')

    robot_description_raw = xacro.process_file(xacro_file).toxml()
    # 4. Define the Robot State Publisher (The missing node)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_raw,
            'use_sim_time': use_sim_time
        }]
    )

    # 5. Include Gazebo Launch (The World & Robot)
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_description_share, 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # 6. Include Nav2 Bringup
    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': nav_params_path,
            'autostart': 'true',
            'map': map_yaml_path
        }.items()
    )

    # 7. Include RViz
    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'rviz_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'rviz_config': rviz_config_path
        }.items()
    )

    # 8. Your AI Agent Node
    ai_agent_node = Node(
        package='warehouse_ai_agent',
        executable='warehouse_agent',
        name='warehouse_ai_agent',
        output='screen',
        parameters=[agent_config_path]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        gazebo_launch,
        robot_state_publisher,
        navigation_launch,
        rviz_launch,
        ai_agent_node
    ])