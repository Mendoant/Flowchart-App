export interface Task {
  id: string;
  name: string;
  time: number;
  skill?: string;
  equipment?: string;
  precedence: string[];
}

export interface Station {
  id: string;
  tasks: string[];
  total_time: number;
  idle_time: number;
}

export interface LineAnalysis {
  total_work_content: number;
  critical_path_time: number;
  theoretical_min_stations: number;
  bottleneck_tasks: string[];
  parallelizable_tasks: string[][];
}

export interface AssemblyLine {
  id: string;
  name: string;
  tasks: Task[];
  edges: { source: string; target: string }[];
}
