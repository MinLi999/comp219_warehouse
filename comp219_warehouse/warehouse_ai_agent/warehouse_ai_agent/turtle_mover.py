import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
from turtlesim.msg import Pose
import math

class TurtleMover(Node):
    def __init__(self):
        super().__init__('turtle_mover')
        self.goal = None
        self.current_pose = None
        
        self.sub_goal = self.create_subscription(PoseStamped, '/hospital_goal', self.goal_callback, 10)
        self.sub_pose = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.pub_vel = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        self.create_timer(0.1, self.control_loop)

    def goal_callback(self, msg):
        self.goal = msg.pose.position
        self.get_logger().info(f"New Goal Received: {self.goal.x}, {self.goal.y}")

    def pose_callback(self, msg):
        self.current_pose = msg

    def control_loop(self):
        if not self.goal or not self.current_pose:
            return

        dist = math.sqrt((self.goal.x - self.current_pose.x)**2 + (self.goal.y - self.current_pose.y)**2)
        
        msg = Twist()
        if dist > 0.1:
            # 1. Calculate target angle
            angle_to_goal = math.atan2(self.goal.y - self.current_pose.y, self.goal.x - self.current_pose.x)
            
            # 2. Calculate raw error
            angle_error = angle_to_goal - self.current_pose.theta
            
            # 3. CRITICAL: Normalize the angle error to [-pi, pi]
            # This prevents the "infinite spinning" bug
            while angle_error > math.pi:
                angle_error -= 2.0 * math.pi
            while angle_error < -math.pi:
                angle_error += 2.0 * math.pi

            # 4. Apply gains (reduce linear slightly to help the turn)
            msg.linear.x = min(1.0 * dist, 2.0) # Cap the speed
            msg.angular.z = 5.0 * angle_error   # Turn toward error
        else:
            self.get_logger().info("Goal Reached!")
            # Publish one final empty twist to stop the motors
            self.pub_vel.publish(Twist()) 
            self.goal = None 
            return # Exit early so we don't publish a non-zero message below
            
        self.pub_vel.publish(msg)

def main():
    rclpy.init()
    rclpy.spin(TurtleMover())
    rclpy.shutdown()