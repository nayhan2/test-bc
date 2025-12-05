"""
Utility Helper Functions
"""

import json
from datetime import datetime
from typing import Any


def format_timestamp(timestamp: float) -> str:
    """
    Format Unix timestamp to readable string
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Formatted date string
    """
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def is_valid_hash(hash_string: str, difficulty: int) -> bool:
    """
    Check if hash meets difficulty requirement
    
    Args:
        hash_string: Hash to validate
        difficulty: Required number of leading zeros
        
    Returns:
        True if hash is valid, False otherwise
    """
    return hash_string.startswith('0' * difficulty)


def serialize_for_json(obj: Any) -> str:
    """
    Serialize object to JSON string
    
    Args:
        obj: Object to serialize
        
    Returns:
        JSON string
    """
    return json.dumps(obj, sort_keys=True, indent=2)


def calculate_total_supply(blocks: list, mining_reward: float) -> float:
    """
    Calculate total cryptocurrency supply
    
    Args:
        blocks: List of blocks
        mining_reward: Reward per block
        
    Returns:
        Total supply
    """
    # Exclude genesis block (index 0)
    mined_blocks = len([b for b in blocks if b.get('index', 0) > 0])
    return mined_blocks * mining_reward
