from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.task import Task
from app.models.station import StationAssignment

class AssemblyLine(BaseModel):
    """Complete assembly line model"""
    id: str = Field(..., description="Unique line identifier")
    name: str = Field(..., description="Line name")
    tasks: List[Task] = Field(default_factory=list)
    edges: List[dict] = Field(
        default_factory=list,
        description="Precedence relationships (source, target)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "line_001",
                "name": "Engine Assembly Line",
                "tasks": [],
                "edges": [{"source": "T1", "target": "T2"}]
            }
        }

class LineAnalysis(BaseModel):
    """Results from analyzing an assembly line"""
    total_work_content: float = Field(..., description="Sum of all task times")
    critical_path_time: float = Field(..., description="Longest path through precedence")
    theoretical_min_stations: int = Field(..., description="Minimum stations needed")
    bottleneck_tasks: List[str] = Field(default_factory=list)
    parallelizable_tasks: List[List[str]] = Field(
        default_factory=list,
        description="Groups of tasks that can be done in parallel"
    )
    
class BalanceRequest(BaseModel):
    """Request to balance an assembly line"""
    line: AssemblyLine
    target_cycle_time: float = Field(..., gt=0, description="Desired cycle time")
    max_stations: Optional[int] = Field(None, description="Maximum number of stations")
    method: str = Field("greedy", description="Balancing method: 'greedy' or 'ilp'")
