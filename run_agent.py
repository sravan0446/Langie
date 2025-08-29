from src.agent import LangGraphAgent
from src.state import Priority
import json


def run_example(example_name, input_data):
    print(f"\n{'=' * 50}")
    print(f"RUNNING EXAMPLE: {example_name}")
    print(f"{'=' * 50}")

    agent = LangGraphAgent("src/config/agent_config.yaml")
    final_state = agent.run(input_data)

    print(f"\n=== {example_name} - FINAL PAYLOAD ===")
    print(json.dumps(final_state, indent=2, default=str))

    # Check if escalation occurred
    escalation = final_state.get("escalation_required", False)
    print(f"\nEscalation Required: {escalation}")

    return final_state


def main():
    # Example 1: Should ask clarification and escalate (short query with question)
    example1_input = {
        "customer_name": "John Doe",
        "email": "john.doe@example.com",
        "query": " I'm having trouble logging into my account. This is urgent as I need to access my premium subscription features. My email is john.smith@email.com and my account ID is ACCT12345 ",
        "priority": Priority.CRITICAL,
        "ticket_id": "12345"
    }

    # Example 2: Should not ask clarification and not escalate (detailed query)
    example2_input = {
        "customer_name": "Jane Smith",
        "email": "jane.smith@example.com",
        "query": "I need to reset my password because I forgot it. I tried using the forgot password link but did not receive the email. Can you help me with this? I have already checked my spam folder.",
        # Detailed enough -> no clarification
        "priority": Priority.LOW,
        "ticket_id": "67890"
    }

    # Run both examples
    result1 = run_example("Example 1", example1_input)
    result2 = run_example("Example 2", example2_input)

    # Summary
    print(f"\n{'=' * 50}")
    print("SUMMARY")
    print(f"{'=' * 50}")
    print(f"Example 1 - Escalation: {result1.get('escalation_required')}")
    print(f"Example 2 - Escalation: {result2.get('escalation_required')}")


if __name__ == "__main__":
    main()