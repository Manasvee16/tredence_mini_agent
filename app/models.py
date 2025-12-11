from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class NodeConfig(BaseModel):
    id: str
    tool_name: str 

class EdgeConfig(BaseModel):
    from_node: str
    # CHANGE IS HERE: We added Optional[...] = None so it accepts null
    to_node: Optional[str] = None 
    condition: Optional[str] = None

class GraphCreateRequest(BaseModel):
    nodes: List[NodeConfig]
    edges: List[EdgeConfig]
    start_node: str

class WorkflowRunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any]
