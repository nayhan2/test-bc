"""
Block Model
Represents a single block in the blockchain
"""

import hashlib
import json
import time
from typing import List, Dict, Any
from .transaction import Transaction


class Block:
    """Represents a block in the blockchain"""
    
    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        previous_hash: str,
        timestamp: float = None,
        nonce: int = 0
    ):
        """
        Initialize a new block
        
        Args:
            index: Position of the block in the chain
            transactions: List of transactions in this block
            previous_hash: Hash of the previous block
            timestamp: Block creation timestamp (defaults to current time)
            nonce: Proof-of-work nonce
        """
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calculate the SHA-256 hash of the block
        
        Returns:
            Hexadecimal hash string
        """
        # Create a dictionary of block data
        block_data = {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce
        }
        
        # Convert to JSON string and encode
        block_string = json.dumps(block_data, sort_keys=True)
        
        # Calculate SHA-256 hash
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """
        Mine the block using proof-of-work
        
        Args:
            difficulty: Number of leading zeros required in hash
        """
        target = '0' * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"Block mined: {self.hash}")
    
    def is_valid(self) -> bool:
        """
        Validate the block
        
        Returns:
            True if block is valid, False otherwise
        """
        # Check if hash is correct
        if self.hash != self.calculate_hash():
            return False
        
        # Validate all transactions
        for transaction in self.transactions:
            if not transaction.is_valid():
                return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert block to dictionary
        
        Returns:
            Dictionary representation of the block
        """
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'hash': self.hash
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Block':
        """
        Create block from dictionary
        
        Args:
            data: Dictionary containing block data
            
        Returns:
            Block instance
        """
        transactions = [Transaction.from_dict(tx) for tx in data['transactions']]
        
        block = cls(
            index=data['index'],
            transactions=transactions,
            previous_hash=data['previous_hash'],
            timestamp=data['timestamp'],
            nonce=data['nonce']
        )
        
        # Set the hash from saved data
        block.hash = data['hash']
        
        return block
    
    def __repr__(self) -> str:
        """String representation of the block"""
        return f"Block(index={self.index}, hash={self.hash[:10]}..., transactions={len(self.transactions)})"
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        return f"Block #{self.index} [{self.hash[:10]}...] with {len(self.transactions)} transaction(s)"
