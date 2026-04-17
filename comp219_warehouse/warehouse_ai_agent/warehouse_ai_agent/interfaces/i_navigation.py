from abc import ABC, abstractmethod

class INavigationProvider(ABC):
    @abstractmethod
    def move_to_pose(self, x: float, y: float, theta: float):
        """Sends a goal to the robot to move to a specific coordinate."""
        pass

    @abstractmethod
    def is_goal_reached(self) -> bool:
        """Checks if the robot has reached its destination."""
        pass