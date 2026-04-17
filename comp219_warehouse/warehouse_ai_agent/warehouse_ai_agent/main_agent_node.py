import os
import sys
import threading
import rclpy
from dotenv import load_dotenv
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from warehouse_ai_agent.graph.workflow import create_hospital_graph
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

# Inside your __init__
# If you have nav2_simple_commander installed, it's better for status feedback
# from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

load_dotenv()

class WarehouseAIAgent(Node):
    def __init__(self):
        super().__init__('warehouse_ai_agent')
        
        # 1. Load coordinates from your parameters (mapped in your launch/yaml)
        self.declare_parameters(
            namespace='',
            parameters=[
                ('room1', [0.0, 0.0, 0.0]),
                ('room2', [0.0, 0.0, 0.0]),
                ('room3', [0.0, 0.0, 0.0]),
                ('room4', [0.0, 0.0, 0.0]),
                ('it_service_desk', [0.0, 0.0, 0.0])
            ]
        )

        # 2. Initialize Components
        self.graph = create_hospital_graph()
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)
        
        self._action_handlers = {
            "PROCEED": self._handle_navigation,
            "ABORT": self._handle_abort,
            "INFO": self._handle_information
        }

        # 3. Security & Feedback
        self.check_api_link()

        # 4. Start Terminal Listener
        self.input_thread = threading.Thread(target=self.terminal_listener, daemon=True)
        self.input_thread.start()
        self.navigator = BasicNavigator()

    def check_api_link(self):
        key = os.getenv("MISTRAL_API_KEY")
        if key:
            self.get_logger().info(f"🔑 AI Brain Link: Connected (Key: {key[:4]}...)")
        else:
            self.get_logger().error("❌ AI Brain Link: FAILED. Check your .env file!")

    def terminal_listener(self):
        self.get_logger().info("--- Warehouse AI Agent Active ---")
        while rclpy.ok():
            try:
                user_query = input("\n🤖 How can I help? > ").strip()
                if not user_query: continue
                if user_query.lower() in ['exit', 'quit']:
                    rclpy.try_shutdown()
                    break
                
                self.run_mission(user_query)
            except Exception as e:
                self.get_logger().error(f"Listener Error: {e}")
                break

    def run_mission(self, user_query: str):
        self.get_logger().info(f">>> Thinking: '{user_query}'")
        
        try:
            # 1. Graph Invoke
            # Note: We pass the params to the graph so the AI knows the real coordinates
            initial_state = {
                "user_input": user_query, 
                "history": [],
                "available_locations": self.get_warehouse_map() 
            }
            final_state = self.graph.invoke(initial_state)

            # 2. Action Selection (Strategy Pattern)
            decision = final_state.get("final_decision", "ABORT")
            handler = self._action_handlers.get(decision, self._handle_abort)
            handler(final_state)

        except Exception as e:
            self.get_logger().error(f"💥 Mission Failure: {e}")

    def get_warehouse_map(self):
        """Helper to package ROS params for the LLM"""
        return {
            "room1": self.get_parameter('room1').value,
            "room2": self.get_parameter('room2').value,
            "room3": self.get_parameter('room3').value,
            "room4": self.get_parameter('room4').value,
            "it_service_desk": self.get_parameter('it_service_desk').value,
        }

    def _handle_navigation(self, state):
        coords = state.get("coords") or state.get("target_pose")
        loc_name = state.get("location_name") or "Target"
        
        if coords and len(coords) >= 2:
            self.publish_goal(coords[0], coords[1], loc_name)
        else:
            self._handle_abort(state)

    def _handle_abort(self, state):
        reason = state.get("reasoning", "Safety check failed.")
        self.get_logger().warn(f"🛑 Mission Aborted: {reason}")

    def _handle_information(self, state):
        self.get_logger().info(f"ℹ️ AI Info: {state.get('response')}")

    def publish_goal(self, x, y, label):
        # 1. Check if Nav2 is ready (Wait for servers to be 'Active')
        # Note: You can also call this once in __init__ to ensure everything is up
        # If calling here, it ensures the robot is localized before sending the goal.
        
        # Proper method for checking/waiting for the stack
        # self.navigator.waitUntilNav2Active() 
        
        # 2. Construct the Message
        msg = PoseStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "map"
        msg.pose.position.x = float(x)
        msg.pose.position.y = float(y)
        msg.pose.orientation.w = 1.0 
        
        # 3. USE THE NAVIGATOR
        self.get_logger().info(f"🚀 AI Agent sending action goal to {label} at [{x}, {y}]")
        self.navigator.goToPose(msg)

        # 4. Check if the goal was accepted
        if not self.navigator.isTaskComplete():
            self.get_logger().info(f"✔ Goal accepted! Robot is navigating to {label}...")

def main(args=None):
    rclpy.init(args=args)
    node = WarehouseAIAgent()
    
    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()