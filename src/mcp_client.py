from typing import Dict, Any, Callable
from .state import SupportState
from .abilities import common_abilities, atlas_abilities


class MCPClient:
    """Mock MCP Client for ability execution"""

    def __init__(self):
        self.common_abilities = {
            "parse_request_text": common_abilities.parse_request_text,
            "normalize_fields": common_abilities.normalize_fields,
            "add_flags_calculations": common_abilities.add_flags_calculations,
            "solution_evaluation": common_abilities.solution_evaluation,
            "response_generation": common_abilities.response_generation
        }

        self.atlas_abilities = {
            "extract_entities": atlas_abilities.extract_entities,
            "enrich_records": atlas_abilities.enrich_records,
            "clarify_question": atlas_abilities.clarify_question,
            "extract_answer": atlas_abilities.extract_answer,
            "knowledge_base_search": atlas_abilities.knowledge_base_search,
            "escalation_decision": atlas_abilities.escalation_decision,
            "update_ticket": atlas_abilities.update_ticket,
            "close_ticket": atlas_abilities.close_ticket,
            "execute_api_calls": atlas_abilities.execute_api_calls,
            "trigger_notifications": atlas_abilities.trigger_notifications
        }

    def execute_ability(self, ability_name: str, state: SupportState, server_type: str) -> Dict[str, Any]:
        """Execute ability through appropriate MCP server"""
        try:
            if server_type == "COMMON":
                ability_func = self.common_abilities.get(ability_name)
            elif server_type == "ATLAS":
                ability_func = self.atlas_abilities.get(ability_name)
            else:
                raise ValueError(f"Unknown server type: {server_type}")

            if ability_func:
                return ability_func(state)
            else:
                raise ValueError(f"Ability not found: {ability_name}")
        except Exception as e:
            print(f"Error executing {ability_name}: {str(e)}")
            return {}