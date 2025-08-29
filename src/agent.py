from typing import Dict, Any, List, Literal
from langgraph.graph import StateGraph, END
from .state import SupportState
from .mcp_client import MCPClient
import yaml
import os


class LangGraphAgent:
    """
    A customer support agent built using LangGraph that processes support tickets
    through a series of defined stages. The agent manages state, interacts with
    mocked services (MCPClient), and uses conditional logic to handle different
    scenarios like escalation.
    """

    def __init__(self, config_path: str = "src/config/agent_config.yaml"):
        """Initializes the agent, loading configuration and building the graph."""
        self.mcp_client = MCPClient()
        self.config = self.load_config(config_path)
        self.graph = self.build_graph()

    def load_config(self, config_path: str) -> Dict[str, Any]:
        """Loads the agent's configuration from a YAML file."""
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def build_graph(self) -> StateGraph:
        """
        Builds the computational graph of the support workflow using StateGraph.
        This defines all the stages (nodes) and the transitions (edges) between them.
        """
        workflow = StateGraph(SupportState)

        # Define all nodes that represent a stage in the workflow
        workflow.add_node("INTAKE", self.intake_stage)
        workflow.add_node("UNDERSTAND", self.understand_stage)
        workflow.add_node("PREPARE", self.prepare_stage)
        workflow.add_node("ASK", self.ask_stage)
        workflow.add_node("WAIT", self.wait_stage)
        workflow.add_node("RETRIEVE", self.retrieve_stage)
        workflow.add_node("DECIDE", self.decide_stage)
        workflow.add_node("UPDATE", self.update_stage)
        workflow.add_node("CREATE", self.create_stage)
        workflow.add_node("DO", self.do_stage)
        workflow.add_node("COMPLETE", self.complete_stage)

        # Set the entry point of the workflow
        workflow.set_entry_point("INTAKE")

        # Define the edges that connect the nodes, forming the workflow path
        workflow.add_edge("INTAKE", "UNDERSTAND")
        workflow.add_edge("UNDERSTAND", "PREPARE")

        # After PREPARE, the graph must decide whether to ask for clarification
        # or proceed directly to retrieving information.
        workflow.add_conditional_edges(
            "PREPARE",
            self.should_ask_clarification,
            {
                "ask": "ASK",
                "retrieve": "RETRIEVE"
            }
        )

        # The 'ask for clarification' path involves asking and then waiting for a response
        workflow.add_edge("ASK", "WAIT")
        workflow.add_edge("WAIT", "RETRIEVE")

        # After retrieving information, the agent decides on the next steps
        workflow.add_edge("RETRIEVE", "DECIDE")

        # After DECIDE, the graph must decide whether to escalate or resolve.
        # This is the core non-deterministic step for escalation.
        workflow.add_conditional_edges(
            "DECIDE",
            self.should_escalate,
            {
                # In both cases, we go to UPDATE. The 'escalation_required' flag in the
                # state will determine the actual operations performed in later stages.
                "escalate": "UPDATE",
                "resolve": "UPDATE"
            }
        )

        # After updating the ticket, we generate a response and execute actions
        workflow.add_edge("UPDATE", "CREATE")
        workflow.add_edge("CREATE", "DO")
        workflow.add_edge("DO", "COMPLETE")

        # The final stage is COMPLETE, which then transitions to the end of the workflow
        workflow.add_edge("COMPLETE", END)

        # Compile the graph into a runnable object
        return workflow.compile()

    def should_ask_clarification(self, state: SupportState) -> Literal["ask", "retrieve"]:
        """
        Decision node: Determines if the agent needs to ask the user for more information.
        """
        query = state.get("query", "")
        # Simple logic: if the query is very short or contains a question, ask for clarification.
        if len(query) < 20:
            print("Decision: Clarification needed (query is short or contains a question).")
            return "ask"
        else:
            print("Decision: No clarification needed.")
            return "retrieve"

    def should_escalate(self, state: SupportState) -> Literal["escalate", "resolve"]:
        """
        Decision node: Determines if the ticket needs to be escalated to a human agent.
        The `escalation_required` flag is set during the 'DECIDE' stage.
        """
        escalation_required = state.get("escalation_required", False)
        score = state.get("solution_score", 0)

        if escalation_required:
            print(f"Decision: ESCALATE (score: {score}). Ticket requires human intervention.")
            return "escalate"
        else:
            print(f"Decision: RESOLVE (score: {score}). Ticket can be handled automatically.")
            return "resolve"

    # --- STAGE DEFINITIONS ---

    def intake_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 1: INTAKE ===")
        print("✓ Payload accepted")
        return state

    def understand_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 2: UNDERSTAND ===")
        abilities = self.config['stages']['UNDERSTAND']['abilities']
        return self.execute_abilities(abilities, state)

    def prepare_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 3: PREPARE ===")
        abilities = self.config['stages']['PREPARE']['abilities']
        return self.execute_abilities(abilities, state)

    def ask_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 4: ASK ===")
        abilities = self.config['stages']['ASK']['abilities']
        return self.execute_abilities(abilities, state)

    def wait_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 5: WAIT ===")
        abilities = self.config['stages']['WAIT']['abilities']
        return self.execute_abilities(abilities, state)

    def retrieve_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 6: RETRIEVE ===")
        abilities = self.config['stages']['RETRIEVE']['abilities']
        return self.execute_abilities(abilities, state)

    def decide_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 7: DECIDE (Non-deterministic) ===")
        # This stage evaluates the query and makes a decision on whether to escalate.
        # 1. Evaluate the solution to get a score.
        state.update(self.mcp_client.execute_ability("solution_evaluation", state, "COMMON"))
        # 2. Based on the score, decide if escalation is required.
        state.update(self.mcp_client.execute_ability("escalation_decision", state, "ATLAS"))
        return state

    def update_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 8: UPDATE ===")
        # This stage is now intelligent. It updates the ticket status differently
        # depending on whether escalation is required.

        # Always update the ticket status first.
        state.update(self.mcp_client.execute_ability("update_ticket", state, "ATLAS"))

        # Only close the ticket if it's NOT being escalated.
        if not state.get("escalation_required", False):
            print("Ticket is being resolved, proceeding to close.")
            state.update(self.mcp_client.execute_ability("close_ticket", state, "ATLAS"))
        else:
            print("Ticket is being escalated, skipping ticket closure.")

        return state

    def create_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 9: CREATE ===")
        # Generates the appropriate response for the customer, which will differ
        # if the ticket is escalated or resolved.
        abilities = self.config['stages']['CREATE']['abilities']
        return self.execute_abilities(abilities, state)

    def do_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 10: DO ===")
        # This stage is also intelligent. It should only execute automated actions
        # (like API calls) if the ticket has been successfully resolved.
        if not state.get("escalation_required", False):
            print("Executing automated actions for resolved ticket.")
            abilities = self.config['stages']['DO']['abilities']
            return self.execute_abilities(abilities, state)
        else:
            print("Skipping automated actions for escalated ticket.")
            return state

    def complete_stage(self, state: SupportState) -> Dict[str, Any]:
        print("\n=== STAGE 11: COMPLETE ===")
        print("✓ Workflow finished. Final payload generated.")
        return state

    def execute_abilities(self, abilities: List[Dict[str, str]], state: SupportState) -> Dict[str, Any]:
        """A helper function to run a list of abilities for a given stage."""
        for ability in abilities:
            if ability['server'] == 'STATE':
                continue
            result = self.mcp_client.execute_ability(
                ability['name'], state, ability['server']
            )
            state.update(result)
        return state

    def run(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the agent's workflow from the initial state."""
        print("Starting LangGraph Agent workflow...")
        final_state = self.graph.invoke(initial_state)
        print("\nWorkflow completed successfully!")
        return final_state
