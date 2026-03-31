#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

class AutoMapper(Node):
    def __init__(self):
        super().__init__('auto_mapper')
        self.publisher_ = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.move_robot)
        self.get_logger().info('Automatic cruise mapping script has been activated....')

    def move_robot(self):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        msg.twist.linear.x = 0.3   # Forward speed (m/s) (m/s)
        msg.twist.angular.z = 0.3  # Angular velocity (rad/s), making it go in a large circle
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = AutoMapper()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Automatic cruise mapping script has been stopped manually.')
    finally:
        # Before stopping, issue a zero speed command to allow the robot to come to a complete halt.
        stop_msg = TwistStamped()
        stop_msg.header.stamp = node.get_clock().now().to_msg()
        stop_msg.header.frame_id = 'base_link'
        node.publisher_.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()