from pydantic import BaseModel, Field, AliasChoices
from typing import List, Optional, Literal

class NavigationGoal(BaseModel):
    location_name: str = Field(description="The name of the room or area")
    coords: List[float] = Field(description="The [x, y, theta] coordinates from the map")
    status: str = Field(description="Either 'success' or 'error'")
    message: Optional[str] = Field(None, description="Error message if location is unknown")


class ClassificationSchema(BaseModel):
    # This will look for 'intent' first, then 'classification' as a backup
    intent: Literal["nav", "info", "off_topic"] = Field(
        validation_alias=AliasChoices('intent', 'classification'),
        description="The category of the user request."
    )
    reasoning: str = Field(description="Brief explanation")



class DispatchSchema(BaseModel):
    location: str = Field(description="The name of the room")
    coords: List[float] = Field(description="[x, y, theta] coordinates")
    status: str = Field(description="'success' or 'error'")
    message: str = Field(default="", description="Error message if any")



class ValidatorSchema(BaseModel):
    is_safe: bool = Field(description="True if coordinates match ground truth exactly")
    reasoning: str = Field(description="Explanation of the coordinate cross-check")
    final_decision: str = Field(default="PROCEED", description="Final instruction for the robot (e.g., PROCEED or ABORT)")