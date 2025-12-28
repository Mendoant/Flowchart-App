from pydantic import BaseModel, Field
from typing import List

class Station(BaseModel):
    """Represents a workstation in the balanced line"""
    id: str = Field(..., description="Station identifier (e.g., 'S1', 'S2')")
    tasks: List[str] = Field(
        default_factory=list,
        description="List of task IDs assigned to this station"
    )
    total_time: float = Field(0.0, ge=0, description="Sum of all task times")
    idle_time: float = Field(0.0, ge=0, description="Idle time in the cycle")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "S1",
                "tasks": ["T1", "T2"],
                "total_time": 92.0,
                "idle_time": 8.0
            }
        }

class StationAssignment(BaseModel):
    """Complete station assignment with performance metrics"""
    stations: List[Station]
    cycle_time: float = Field(..., description="Target cycle time")
    efficiency: float = Field(..., ge=0, le=1, description="Line efficiency")
    balance_delay: float = Field(..., ge=0, description="Balance delay percentage")
    smoothness_index: float = Field(..., ge=0, description="Smoothness index")
    
    class Config:
        json_schema_extra = {
            "example": {
                "stations": [
                    {
                        "id": "S1",
                        "tasks": ["T1", "T2"],
                        "total_time": 95.0,
                        "idle_time": 5.0
                    }
                ],
                "cycle_time": 100.0,
                "efficiency": 0.95,
                "balance_delay": 2.5,
                "smoothness_index": 0.98
            }
        }
