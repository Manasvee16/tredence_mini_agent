import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse # <--- Import this
from app.models import GraphCreateRequest, WorkflowRunRequest
from app.engine import GRAPHS, RUNS, WorkflowEngine

app = FastAPI(title="Mini Agent Engine")

@app.post("/graph/create")
def create_graph(graph: GraphCreateRequest):
    graph_id = str(uuid.uuid4())
    GRAPHS[graph_id] = WorkflowEngine(graph)
    return {"graph_id": graph_id, "message": "Graph created successfully"}

@app.post("/graph/run")
def run_workflow(request: WorkflowRunRequest):
    if request.graph_id not in GRAPHS:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    # CORRECTED LINE BELOW:
    engine = GRAPHS[request.graph_id] 
    
    final_state = engine.run(request.initial_state)
    
    run_id = str(uuid.uuid4())
    RUNS[run_id] = final_state
    
    return {
        "run_id": run_id,
        "final_state": final_state
    }

@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    if run_id not in RUNS:
        raise HTTPException(status_code=404, detail="Run ID not found")
    return RUNS[run_id]

# --- IMPROVEMENT 1: Visualizer Endpoint ---
@app.get("/graph/visualize/{graph_id}", response_class=PlainTextResponse)
def visualize_graph(graph_id: str):
    if graph_id not in GRAPHS:
        raise HTTPException(status_code=404, detail="Graph not found")
    
    return GRAPHS[graph_id].to_mermaid()
