from typing import Dict, Any, List
from ..state import SupportState

def extract_entities(state: SupportState) -> Dict[str, Any]:
    """Identify product, account, dates"""
    # Mock entity extraction
    entities = {
        "products": ["ProductA"] if "product" in state["query"].lower() else [],
        "account_mentioned": "account" in state["query"].lower(),
        "dates": ["2024-01-20"] if "january" in state["query"].lower() else []
    }
    print("✓ extract_entities executed (ATLAS)")
    return {"extracted_entities": entities}

def enrich_records(state: SupportState) -> Dict[str, Any]:
    """Add SLA, historical ticket info"""
    enriched_data = {
        "sla_due_date": "2024-01-17T23:59:59Z",
        "previous_tickets": 2,
        "customer_tier": "premium" if "premium" in state["email"] else "standard"
    }
    print("✓ enrich_records executed (ATLAS)")
    return {"enriched_data": enriched_data}

def clarify_question(state: SupportState) -> Dict[str, Any]:
    """Request missing information"""
    question = "Can you please provide more details about the issue you're experiencing?"
    print("✓ clarify_question executed (ATLAS)")
    return {"clarification_question": question}

def extract_answer(state: SupportState) -> Dict[str, Any]:
    """Wait and capture concise response"""
    # Simulate waiting for and extracting answer
    answer = "The issue occurs when I click the submit button twice."
    print("✓ extract_answer executed (ATLAS)")
    return {"clarification_answer": answer}

def knowledge_base_search(state: SupportState) -> Dict[str, Any]:
    """Lookup KB or FAQ"""
    kb_results = [
        {"title": "How to resolve submission issues", "url": "https://kb.example.com/123"},
        {"title": "Common product errors", "url": "https://kb.example.com/456"}
    ]
    print("✓ knowledge_base_search executed (ATLAS)")
    return {"kb_results": kb_results}

def escalation_decision(state: SupportState) -> Dict[str, Any]:
    """Assign to human agent if score <90"""
    escalation_required = state.get("solution_score", 0) < 90
    print(f"✓ escalation_decision executed - Escalation: {escalation_required} (ATLAS)")
    return {"escalation_required": escalation_required}

def update_ticket(state: SupportState) -> Dict[str, Any]:
    """Modify status, fields, priority"""
    status = "escalated" if state.get("escalation_required") else "in_progress"
    print(f"✓ update_ticket executed - Status: {status} (ATLAS)")
    return {"ticket_status": status}

def close_ticket(state: SupportState) -> Dict[str, Any]:
    """Mark issue resolved"""
    print("✓ close_ticket executed (ATLAS)")
    return {"ticket_status": "closed"}

def execute_api_calls(state: SupportState) -> Dict[str, Any]:
    """Trigger CRM/order system actions"""
    api_results = {
        "crm_update": "success",
        "timestamp": "2024-01-15T11:30:00Z"
    }
    print("✓ execute_api_calls executed (ATLAS)")
    return {"api_call_results": api_results}

def trigger_notifications(state: SupportState) -> Dict[str, Any]:
    """Notify customer"""
    print("✓ trigger_notifications executed (ATLAS)")
    return {"notifications_sent": True}