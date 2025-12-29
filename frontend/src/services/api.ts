import axios from 'axios';
import { Task, AssemblyLine, LineAnalysis } from '../types';

const API_BASE = '/api';

export const flowAPI = {
  validateFlow: async (tasks: Task[]) => {
    const response = await axios.post(`${API_BASE}/flow/validate`, tasks);
    return response.data;
  },

  analyzeFlow: async (line: AssemblyLine): Promise<LineAnalysis> => {
    const response = await axios.post(`${API_BASE}/flow/analyze`, line);
    return response.data;
  },

  getExampleFlow: async (): Promise<AssemblyLine> => {
    const response = await axios.get(`${API_BASE}/flow/example`);
    return response.data;
  },
};
