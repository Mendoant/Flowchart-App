from pydantic import BaseModel, Field
from typing import List, Optional

class Task(BaseModel):
    """Represents a single task/operation in the assembly flow"""
    id: str = Field(..., description="Unique task identifier (e.g., 'T1', 'T2')")
    name: str = Field(..., description="Human-readable task name")
    time: float = Field(..., ge=0, description="Task time in seconds")
    skill: Optional[str] = Field(None, description="Required skill level or type")
    equipment: Optional[str] = Field(None, description="Required equipment")
    precedence: List[str] = Field(
        default_factory=list,
        description="List of task IDs that must be completed before this task"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "T1",
                "name": "Install actuator",
                "time": 45.0,
                "skill": "mechanical",
                "equipment": "press",
                "precedence": []
            }
        }

class TaskNode(BaseModel):
    """Extended task model with position data for frontend visualization"""
    task: Task
    position: dict = Field(..., description="X, Y coordinates for visualization")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task": {
                    "id": "T1",
                    "name": "Install actuator",
                    "time": 45.0,
                    "skill": "mechanical",
                    "equipment": "press",
                    "precedence": []
                },
                "position": {"x": 100, "y": 200}
            }
        }
