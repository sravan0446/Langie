# Lang Graph Customer Support Agent

This project implements an intelligent, multi-stage customer support agent using the LangGraph library. The agent models a complex support workflow as a graph, where each node represents a distinct stage in processing a customer ticket. It demonstrates state persistence, integration with mock services, and conditional logic for dynamic routing.

## ✨ Features

-   **Graph-Based Workflow**: The entire 11-stage customer support flow is modeled as a directed acyclic graph.
-   **State Persistence**: The agent's state (`SupportState`) is seamlessly passed and updated across all stages of the workflow.
-   **Deterministic & Non-Deterministic Stages**: Includes sequential stages (e.g., `UNDERSTAND` -> `PREPARE`) and conditional, non-deterministic stages (e.g., `DECIDE` to escalate or resolve).
-   **MCP Client Integration**: Simulates routing requests to different microservices (`COMMON` for internal logic, `ATLAS` for external data interaction) via a mock `MCPClient`.
-   **Conditional Logic**: The agent can dynamically alter its path based on the content of the query, deciding whether to ask for clarification or escalate to a human.
-   **Clear Logging**: Provides detailed console output to trace the agent's execution path and decisions at every stage.

## 📂 Project Structure

```
.
├── requirements.txt
├── run_agent.py
└── src
    ├── agent.py
    ├── mcp_client.py
    ├── state.py
    ├── __init__.py
    ├── abilities
    │   ├── atlas_abilities.py
    │   ├── common_abilities.py
    │   └── __init__.py
    └── config
        └── agent_config.yaml
```

-   **`run_agent.py`**: The main entry point to run the demo. It defines two example customer tickets and executes the agent for each.
-   **`src/agent.py`**: The core of the project. Contains the `LangGraphAgent` class, which defines the graph structure, stages, and conditional logic.
-   **`src/state.py`**: Defines the `SupportState` TypedDict, which is the data structure for persisting state across the graph.
-   **`src/mcp_client.py`**: A mock client that simulates calling different server types (`ATLAS` or `COMMON`) to execute abilities.
-   **`src/abilities/`**: Contains the individual functions (abilities) that are executed at each stage.
-   **`src/config/agent_config.yaml`**: Configuration file that maps stages to their respective abilities and server types.
-   **`requirements.txt`**: A list of all the Python dependencies for this project.

## 🚀 Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃 How to Run

Execute the main script from the root directory of the project:

```bash
python run_agent.py
```

The script will run two predefined examples:
1.  **Example 1**: An urgent query that demonstrates the "escalation" path.
2.  **Example 2**: A detailed query that demonstrates the automated resolution path without escalation.

The console will display detailed logs for each stage of the workflow for both examples, followed by the final structured JSON payload.

## 📊 Workflow Visualization

The agent's workflow can be visualized using the provided `graph.dot` file. You need to have [Graphviz](https://graphviz.org/download/) installed to render it.

Once Graphviz is installed, you can generate a PNG image of the graph with the following command:

```bash
dot -Tpng graph.dot -o workflow.png
```

This will create an image file named `workflow.png` showing the nodes and edges of the agent's logic.
