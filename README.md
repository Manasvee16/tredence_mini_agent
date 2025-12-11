# Mini Agent Workflow Engine

A simplified backend workflow engine inspired by LangGraph. This system allows you to define sequences of steps (Nodes), connect them (Edges), and execute them with a shared state. It supports conditional branching, looping, and tool execution.

## Features
* **Graph-based Execution:** Define nodes and edges dynamically via API.
* **State Management:** Shared state flows between nodes.
* **Conditional Looping:** Supports cycles (e.g., "Loop until quality score > 80").
* **Tool Registry:** Modular architecture to easily add new Python functions.
* **Visualizer:** Built-in Mermaid.js endpoint to visualize workflow logic.
* **Resilience:** Error handling boundaries prevent tool failures from crashing the engine.

## Setup & Run

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd tredence_assignment
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start the server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.
    API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`.

## Usage Example (Option A: Code Review Agent)

1.  **Create Graph:** POST `/graph/create` with the node/edge definition.
2.  **Run Workflow:** POST `/graph/run` with the initial code snippet.
3.  **Visualize:** GET `/graph/visualize/{graph_id}` to see the flowchart.

## Future Improvements
If given more time, I would implement:
* **Persistence:** Use SQLite/PostgreSQL to store graph definitions and run history permanently (currently in-memory).
* **Async Execution:** Use `Celery` or `asyncio` for long-running nodes.
* **WebSockets:** To stream execution logs to the client in real-time.
