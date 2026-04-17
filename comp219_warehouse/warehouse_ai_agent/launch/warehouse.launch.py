import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'warehouse_ai_agent'
    pkg_share = get_package_share_directory(package_name)
    
    # Path to your YAML and Map
    config_path = os.path.join(pkg_share, 'config', 'map_locations.yaml')
    map_path = os.path.join(pkg_share, 'maps', 'map.yaml') # Ensure this path is correct

    # 1. NEW: Include the standard Navigation Bringup
    # This starts AMCL, the Map Server, and the Lifecycle Manager
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map': map_path,
            'use_sim_time': 'True',
            'params_file': os.path.join(get_package_share_directory('nav2_bringup'), 'params', 'nav2_params.yaml')
        }.items()
    )

    # 2. Your existing AI Agent Node
    ai_agent_node = Node(
        package=package_name,
        executable='warehouse_agent',
        name='warehouse_ai_agent',
        output='screen',
        emulate_tty=True,
        parameters=[config_path]
    )

    return LaunchDescription([
        nav2_launch,
        ai_agent_node
    ])