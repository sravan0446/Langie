from typing import Dict, Any
from ..state import SupportState


def parse_request_text(state: SupportState) -> Dict[str, Any]:
    """Convert unstructured request to structured data"""
    # Simple implementation - in real scenario would use NLP
    structured_data = {
        "customer_query": state["query"],
        "urgency_keywords": ["urgent", "asap", "immediately"] if any(
            word in state["query"].lower() for word in ["urgent", "asap", "immediately"]
        ) else []
    }
    print("✓ parse_request_text executed (COMMON)")
    return {"structured_data": structured_data}


def normalize_fields(state: SupportState) -> Dict[str, Any]:
    """Standardize dates, codes, IDs"""
    normalized_data = {
        "priority": state["priority"].upper(),
        "ticket_id": f"TKT-{state['ticket_id']}",
        "received_timestamp": "2024-01-15T10:30:00Z"  # Would use current time in real scenario
    }
    print("✓ normalize_fields executed (COMMON)")
    return {"normalized_fields": normalized_data}


def add_flags_calculations(state: SupportState) -> Dict[str, Any]:
    """Compute priority or SLA risk"""
    flags = {
        "high_priority": state["priority"] in ["high", "critical"],
        "sla_risk": state["priority"] == "critical",
        "requires_follow_up": "follow up" in state["query"].lower()
    }
    print("✓ add_flags_calculations executed (COMMON)")
    return {"flags": flags}


def solution_evaluation(state: SupportState) -> Dict[str, Any]:
    """Score potential solutions 1-100 based on query complexity"""
    query = state["query"].lower()

    # More sophisticated scoring based on various factors
    score = 100  # Start with perfect score

    # Deduct points based on length
    if len(query) < 20:  # Very short query
        score -= 40
    elif len(query) < 50:  # Short query
        score -= 20
    elif len(query) > 100:  # Long query might be complex
        score -= 10

    # Deduct points for technical complexity indicators
    technical_terms = ["error", "bug", "crash", "failure", "timeout", "database", "server", "production"]
    technical_count = sum(1 for term in technical_terms if term in query)
    score -= technical_count * 5

    # Deduct points for urgency indicators
    urgency_terms = ["urgent", "critical", "immediately", "asap", "emergency"]
    urgency_count = sum(1 for term in urgency_terms if term in query)
    score -= urgency_count * 3

    # Ensure score is within bounds
    score = max(50, min(100, score))

    print(f"✓ solution_evaluation executed - Score: {score}/100 (COMMON)")
    return {"solution_score": score}


def response_generation(state: SupportState) -> Dict[str, Any]:
    """Draft customer reply"""
    response = f"""Dear {state['customer_name']},

Thank you for contacting support. We have {'escalated' if state.get('escalation_required') else 'processed'} your request.

Query: {state['query'][:100]}...
{'Your issue has been assigned to a specialist for further investigation.' if state.get('escalation_required') else 'Your issue has been resolved.'}

Best regards,
Support Team"""
    print("✓ response_generation executed (COMMON)")
    return {"response": response}