import json
import os
from typing import Dict, Any, List

def get_agent_config(agent_name: str) -> Dict[str, Any]:
    """
    Loads configuration for a specific agent from agents.json
    """
    config_path = os.path.join(os.path.dirname(__file__), "../../agents.json")
    try:
        with open(config_path, "r") as f:
            agents = json.load(f)
            for agent in agents:
                if agent["name"] == agent_name:
                    return agent
    except Exception as e:
        print(f"Error loading agent config for {agent_name}: {e}")
    
    # Fallback default
    return {"name": agent_name, "model": "anthropic/claude-3.5-sonnet", "temperature": 0.2}
