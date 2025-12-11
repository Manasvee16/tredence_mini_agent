from typing import Dict, Any
from app.models import GraphCreateRequest
from app.tools import TOOL_REGISTRY

# In-memory storage
GRAPHS = {}
RUNS = {}

class WorkflowEngine:
    def __init__(self, config: GraphCreateRequest):
        self.nodes = {n.id: n.tool_name for n in config.nodes}
        self.edges = config.edges
        self.start_node = config.start_node

    def get_next_node(self, current_node_id, state):
        """Determines the next node based on edges and state."""
        candidates = [e for e in self.edges if e.from_node == current_node_id]
        
        for edge in candidates:
            if not edge.condition:
                return edge.to_node
            
            try:
                # Basic condition parsing: "variable operator value"
                key, op, limit = edge.condition.split()
                val = state.get(key, 0)
                limit = int(limit)
                
                if op == "<" and val < limit: return edge.to_node
                if op == ">" and val > limit: return edge.to_node
                if op == ">=" and val >= limit: return edge.to_node
                if op == "<=" and val <= limit: return edge.to_node
            except Exception as e:
                print(f"Condition error: {e}")
                continue
        return None 

    def run(self, initial_state: Dict[str, Any]):
        state = initial_state.copy()
        if "logs" not in state: state["logs"] = []
        
        current_node_id = self.start_node
        steps = 0
        MAX_STEPS = 20 

        while current_node_id and steps < MAX_STEPS:
            steps += 1
            tool_name = self.nodes.get(current_node_id)
            
            if tool_name and tool_name in TOOL_REGISTRY:
                # --- IMPROVEMENT 2: Error Handling ---
                try:
                    func = TOOL_REGISTRY[tool_name]
                    state = func(state)
                except Exception as e:
                    error_msg = f"Error in node '{current_node_id}': {str(e)}"
                    state["error"] = error_msg
                    state["logs"].append(error_msg)
                    break # Stop execution safely
                # -------------------------------------
            
            current_node_id = self.get_next_node(current_node_id, state)
            
        return state

    # --- IMPROVEMENT 1: Visualizer Logic ---
    def to_mermaid(self):
        """Generates a Mermaid.js flowchart string."""
        chart = ["graph TD"]
        
        # Add Nodes
        for node_id, tool in self.nodes.items():
            chart.append(f'    {node_id}["{tool}"]')
            
        # Add Edges
        for edge in self.edges:
            target = edge.to_node if edge.to_node else "End"
            if edge.condition:
                chart.append(f'    {edge.from_node} -- "{edge.condition}" --> {target}')
            else:
                chart.append(f'    {edge.from_node} --> {target}')
        
        # <<< CHECK THIS LINE BELOW >>>
        return "\n".join(chart)
