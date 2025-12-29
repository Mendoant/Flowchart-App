import networkx as nx
from typing import List, Tuple
from app.models.task import Task

class FlowValidator:
    """Validates assembly flow for structural correctness"""
    
    @staticmethod
    def validate_flow(tasks: List[Task]) -> Tuple[bool, List[str]]:
        """
        Validates the assembly flow for common issues
        
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        if not tasks:
            errors.append("Flow must contain at least one task")
            return False, errors
        
        # Build precedence graph
        G = nx.DiGraph()
        task_ids = {task.id for task in tasks}
        
        for task in tasks:
            G.add_node(task.id)
            for pred in task.precedence:
                if pred not in task_ids:
                    errors.append(f"Task {task.id} references non-existent predecessor {pred}")
                else:
                    G.add_edge(pred, task.id)
        
        # Check for cycles
        if not nx.is_directed_acyclic_graph(G):
            cycles = list(nx.simple_cycles(G))
            errors.append(f"Flow contains cycles: {cycles}")
        
        # Check connectivity (optional - depends on requirements)
        if G.number_of_nodes() > 0:
            # Check if there's at least one source (task with no predecessors)
            sources = [n for n in G.nodes() if G.in_degree(n) == 0]
            if not sources:
                errors.append("Flow has no starting task (all tasks have predecessors)")
            
            # Check if there's at least one sink (task with no successors)
            sinks = [n for n in G.nodes() if G.out_degree(n) == 0]
            if not sinks:
                errors.append("Flow has no ending task (all tasks have successors)")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    @staticmethod
    def validate_task_times(tasks: List[Task]) -> Tuple[bool, List[str]]:
        """Validates that all task times are positive"""
        errors = []
        
        for task in tasks:
            if task.time <= 0:
                errors.append(f"Task {task.id} has invalid time: {task.time}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
