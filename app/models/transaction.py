"""
Transaction Model
Represents a transaction in the blockchain
"""

import time
from typing import Dict, Any
from datetime import datetime


class Transaction:
    """Represents a transaction between two parties"""
    
    def __init__(self, sender: str, recipient: str, amount: float, timestamp: float = None):
        """
        Initialize a new transaction
        
        Args:
            sender: Address of the sender
            recipient: Address of the recipient
            amount: Amount to transfer
            timestamp: Transaction timestamp (defaults to current time)
        """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp or time.time()
    
    def is_valid(self) -> bool:
        """
        Validate the transaction
        
        Returns:
            True if transaction is valid, False otherwise
        """
        # Check if all required fields are present
        if not self.sender or not self.recipient:
            return False
        
        # Check if amount is positive
        if self.amount <= 0:
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert transaction to dictionary
        
        Returns:
            Dictionary representation of the transaction
        """
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """
        Create transaction from dictionary
        
        Args:
            data: Dictionary containing transaction data
            
        Returns:
            Transaction instance
        """
        return cls(
            sender=data['sender'],
            recipient=data['recipient'],
            amount=data['amount'],
            timestamp=data.get('timestamp')
        )
    
    def __repr__(self) -> str:
        """String representation of the transaction"""
        return f"Transaction(from={self.sender}, to={self.recipient}, amount={self.amount})"
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        dt = datetime.fromtimestamp(self.timestamp)
        return f"{self.sender} -> {self.recipient}: {self.amount} ({dt.strftime('%Y-%m-%d %H:%M:%S')})"
