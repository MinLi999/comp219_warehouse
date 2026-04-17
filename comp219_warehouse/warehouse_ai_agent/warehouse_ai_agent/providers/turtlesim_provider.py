import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from ..interfaces.i_navigation import INavigationProvider

class TurtlesimProvider(INavigationProvider):
    def __init__(self, node: Node):
        self.node = node
        self.publisher = self.node.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def move_to_pose(self, x: float, y: float, theta: float):
        # For the smoke test, we just send a simple velocity burst
        # In the full version, we'd use a more precise movement loop
        msg = Twist()
        msg.linear.x = 2.0 
        self.publisher.publish(msg)
        self.node.get_logger().info(f"Turtlesim moving towards X:{x}, Y:{y}")

    def is_goal_reached(self) -> bool:
        return True # Simplified for initial smoke test