import yaml
import os
from ament_index_python.packages import get_package_share_directory, PackageNotFoundError

class PromptManager:
    def __init__(self, package_name="warehouse_ai_agent"):
        try:
            # 1. Try to find the installed share directory
            self.package_share = get_package_share_directory(package_name)
        except PackageNotFoundError:
            # 2. Fallback to the direct source path if colcon build failed
            self.package_share = os.path.expanduser(
                '~/project_ws/src/comp219_warehouse-main/comp219_warehouse/warehouse_ai_agent/warehouse_ai_agent'
            )
            print(f"⚠️ Warning: Package '{package_name}' not installed. Using source path: {self.package_share}")

        # Path to the config file (matches your manual move earlier)
        self.map_path = os.path.join(self.package_share, 'config', 'map_locations.yaml')
        self.locations = self.load_map()

    def load_map(self):
        try:
            with open(self.map_path, 'r') as file:
                data = yaml.safe_load(file)
                
                # The YAML has 'warehouse_ai_agent' at the top level
                # then 'ros__parameters' below it.
                node_params = data.get('warehouse_ai_agent', {}).get('ros__parameters', {})
               
                # Use the YAML-defined locations list so new rooms are picked up automatically
                room_keys = node_params.get("locations", [])
                if not room_keys:
                    room_keys = [k for k in node_params.keys() if k not in ["locations", "initial_pose"]]
                
                # Create a dictionary of just the rooms and their [x, y, z]
                extracted_locations = {k: node_params[k] for k in room_keys if k in node_params}
                
                print(f"✅ Successfully loaded {len(extracted_locations)} locations from YAML.")
                return extracted_locations
        except Exception as e:
            print(f"❌ Error parsing YAML at {self.map_path}: {e}")
            return {}

    def get_dispatcher_prompt(self) -> str:
        # Inject the YAML data into the prompt
        location_str = "\n".join([f"- {name}: {coords}" for name, coords in self.locations.items()])
        
        return f"""
        You are the Navigation Dispatcher for a warehouse robot.
        Your job is to extract the destination from the user's request and provide the coordinates.
        
        KNOWN LOCATIONS:
        {location_str}
        
        If the user mentions PCs or monitors, map it to room1.
        If the user mentions laptops, map it to room2.
        If the user mentions accessories, map it to room3.
        If the user mentions cables, map it to room4.
        If the user mentions charging station, map it to charging_station.
        
        If the location is known, respond ONLY in JSON format:
        {{"location": "room_name", "coords": [x, y, theta], "status": "success"}}
        
        If the location is unknown, respond:
        {{"location": "unknown", "coords": [], "status": "error", "message": "I don't know that room."}}
        """
