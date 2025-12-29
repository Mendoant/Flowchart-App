from fastapi import APIRouter, HTTPException
from typing import List
from app.models.task import Task
from app.models.line import AssemblyLine, LineAnalysis
from app.services.validator import FlowValidator
from app.services.graph_analysis import GraphAnalyzer

router = APIRouter()

@router.post("/validate", response_model=dict)
async def validate_flow(tasks: List[Task]):
    """Validate assembly flow for structural correctness"""
    is_valid, errors = FlowValidator.validate_flow(tasks)
    
    if not is_valid:
        return {
            "valid": False,
            "errors": errors
        }
    
    # Also validate task times
    times_valid, time_errors = FlowValidator.validate_task_times(tasks)
    
    return {
        "valid": is_valid and times_valid,
        "errors": errors + time_errors
    }

@router.post("/analyze", response_model=LineAnalysis)
async def analyze_flow(line: AssemblyLine):
    """Analyze assembly line and return IE metrics"""
    # First validate
    is_valid, errors = FlowValidator.validate_flow(line.tasks)
    if not is_valid:
        raise HTTPException(status_code=400, detail={"errors": errors})
    
    # Perform analysis
    analysis = GraphAnalyzer.analyze_line(line.tasks)
    return analysis

@router.get("/example")
async def get_example_flow():
    """Returns an example assembly flow for testing"""
    return {
        "id": "example_001",
        "name": "Simple Assembly Example",
        "tasks": [
            {
                "id": "T1",
                "name": "Pick base component",
                "time": 15.0,
                "skill": "basic",
                "equipment": None,
                "precedence": []
            },
            {
                "id": "T2",
                "name": "Install bracket",
                "time": 25.0,
                "skill": "mechanical",
                "equipment": "screwdriver",
                "precedence": ["T1"]
            },
            {
                "id": "T3",
                "name": "Attach cover",
                "time": 20.0,
                "skill": "basic",
                "equipment": None,
                "precedence": ["T2"]
            },
            {
                "id": "T4",
                "name": "Quality check",
                "time": 10.0,
                "skill": "inspector",
                "equipment": "gauge",
                "precedence": ["T3"]
            }
        ],
        "edges": [
            {"source": "T1", "target": "T2"},
            {"source": "T2", "target": "T3"},
            {"source": "T3", "target": "T4"}
        ]
    }
