import networkx as nx
from typing import List
from app.models.task import Task
from app.models.line import LineAnalysis

class GraphAnalyzer:
    """Analyzes precedence graph for IE metrics"""
    
    @staticmethod
    def analyze_line(tasks: List[Task]) -> LineAnalysis:
        """
        Performs comprehensive analysis of assembly line
        
        Returns:
            LineAnalysis with key metrics
        """
        # Build precedence graph
        G = nx.DiGraph()
        task_dict = {task.id: task for task in tasks}
        
        for task in tasks:
            G.add_node(task.id, time=task.time)
            for pred in task.precedence:
                if pred in task_dict:
                    G.add_edge(pred, task.id)
        
        # Calculate total work content
        total_work_content = sum(task.time for task in tasks)
        
        # Calculate critical path using longest path algorithm
        critical_path_time = GraphAnalyzer._calculate_critical_path(G, task_dict)
        
        # Find bottleneck tasks (highest time tasks)
        sorted_tasks = sorted(tasks, key=lambda t: t.time, reverse=True)
        bottleneck_tasks = [sorted_tasks[0].id] if sorted_tasks else []
        
        # Find parallelizable task groups
        parallelizable = GraphAnalyzer._find_parallel_tasks(G)
        
        # Calculate theoretical minimum stations
        # This is a rough estimate: total_work / critical_path
        theoretical_min_stations = max(1, int(total_work_content / critical_path_time)) if critical_path_time > 0 else 1
        
        return LineAnalysis(
            total_work_content=total_work_content,
            critical_path_time=critical_path_time,
            theoretical_min_stations=theoretical_min_stations,
            bottleneck_tasks=bottleneck_tasks,
            parallelizable_tasks=parallelizable
        )
    
    @staticmethod
    def _calculate_critical_path(G: nx.DiGraph, task_dict: dict) -> float:
        """Calculate critical path time using longest path algorithm"""
        if G.number_of_nodes() == 0:
            return 0.0
        
        try:
            # NetworkX expects negative weights for longest path
            for u, v in G.edges():
                G[u][v]['weight'] = -task_dict[v].time
            
            # Find longest path from any source to any sink
            sources = [n for n in G.nodes() if G.in_degree(n) == 0]
            sinks = [n for n in G.nodes() if G.out_degree(n) == 0]
            
            max_path_length = 0
            for source in sources:
                for sink in sinks:
                    if nx.has_path(G, source, sink):
                        path_length = -nx.shortest_path_length(G, source, sink, weight='weight')
                        # Add source task time
                        path_length += task_dict[source].time
                        max_path_length = max(max_path_length, path_length)
            
            return max_path_length
        except:
            # Fallback: return max single task time
            return max((task.time for task in task_dict.values()), default=0.0)
    
    @staticmethod
    def _find_parallel_tasks(G: nx.DiGraph) -> List[List[str]]:
        """Identify groups of tasks that can be performed in parallel"""
        parallel_groups = []
        
        # Tasks at the same level (same distance from source) can potentially be parallel
        sources = [n for n in G.nodes() if G.in_degree(n) == 0]
        
        for source in sources:
            levels = {}
            for node in nx.descendants(G, source) | {source}:
                try:
                    levels[node] = nx.shortest_path_length(G, source, node)
                except:
                    continue
            
            # Group by level
            level_groups = {}
            for node, level in levels.items():
                if level not in level_groups:
                    level_groups[level] = []
                level_groups[level].append(node)
            
            # Only include groups with more than one task
            for group in level_groups.values():
                if len(group) > 1:
                    parallel_groups.append(group)
        
        return parallel_groups
