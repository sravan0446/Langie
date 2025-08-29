from typing import TypedDict, Optional, List, Dict, Any
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SupportState(TypedDict):
    # Initial payload
    customer_name: str
    email: str
    query: str
    priority: Priority
    ticket_id: str

    # Additional state accumulated through stages
    structured_data: Optional[Dict[str, Any]]
    extracted_entities: Optional[Dict[str, Any]]
    normalized_fields: Optional[Dict[str, Any]]
    enriched_data: Optional[Dict[str, Any]]
    flags: Optional[Dict[str, Any]]
    clarification_answer: Optional[str]
    kb_results: Optional[List[Dict[str, Any]]]
    solution_score: Optional[int]
    escalation_required: Optional[bool]
    ticket_status: Optional[str]
    response: Optional[str]
    api_call_results: Optional[Dict[str, Any]]
    notifications_sent: Optional[bool]
