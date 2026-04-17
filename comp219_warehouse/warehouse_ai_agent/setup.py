from setuptools import find_packages, setup
import os
from glob import glob

# 1. UPDATED NAME
package_name = 'warehouse_ai_agent'

setup(
    name=package_name,
    version='0.0.0',
    # This finds all your sub-folders like agents, graph, utils automatically
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Ensure these point to the actual folder names in your src directory
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
    ],
    install_requires=[
        'setuptools',
        'mistralai',
        'python-dotenv',
        'langgraph',
        'pydantic',
        'pyyaml'
    ],
    zip_safe=True,
    maintainer='edwin',
    maintainer_email='edwin@todo.todo',
    description='Warehouse AI Inventory Manager using LangGraph',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # 2. UPDATED ENTRY POINTS to point to the new folder structure
            'warehouse_agent = warehouse_ai_agent.main_agent_node:main',
            'turtle_mover = warehouse_ai_agent.turtle_mover:main'
        ],
    },
)