"""
Blockchain Model
Manages the entire blockchain
"""

from typing import List, Dict, Any, Optional
from .block import Block
from .transaction import Transaction


class Blockchain:
    """Manages the blockchain and its operations"""
    
    def __init__(self, difficulty: int = 4, mining_reward: float = 10.0):
        """
        Initialize a new blockchain
        
        Args:
            difficulty: Mining difficulty (number of leading zeros)
            mining_reward: Reward for mining a block
        """
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        
        # Create genesis block if chain is empty
        if not self.chain:
            self.create_genesis_block()
    
    def create_genesis_block(self) -> Block:
        """
        Create the first block in the blockchain
        
        Returns:
            The genesis block
        """
        genesis_block = Block(
            index=0,
            transactions=[],
            previous_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        return genesis_block
    
    def get_latest_block(self) -> Block:
        """
        Get the most recent block in the chain
        
        Returns:
            The latest block
        """
        return self.chain[-1] if self.chain else None
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """
        Add a transaction to pending transactions
        
        Args:
            transaction: Transaction to add
            
        Returns:
            True if transaction was added, False otherwise
        """
        if not transaction.is_valid():
            return False
        
        self.pending_transactions.append(transaction)
        return True
    
    def mine_pending_transactions(self, mining_reward_address: str) -> Block:
        """
        Mine all pending transactions into a new block
        
        Args:
            mining_reward_address: Address to receive mining reward
            
        Returns:
            The newly mined block
        """
        # Add mining reward transaction
        reward_transaction = Transaction(
            sender="SYSTEM",
            recipient=mining_reward_address,
            amount=self.mining_reward
        )
        self.pending_transactions.append(reward_transaction)
        
        # Create new block
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        
        # Mine the block
        print(f"Mining block {new_block.index}...")
        new_block.mine_block(self.difficulty)
        
        # Add to chain
        self.chain.append(new_block)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        return new_block
    
    def add_block(self, block: Block) -> bool:
        """
        Add a pre-mined block to the chain (used when loading from database)
        
        Args:
            block: Block to add
            
        Returns:
            True if block was added, False otherwise
        """
        if not block.is_valid():
            return False
        
        # Verify previous hash matches
        if self.chain and block.previous_hash != self.get_latest_block().hash:
            return False
        
        self.chain.append(block)
        return True
    
    def is_chain_valid(self) -> bool:
        """
        Validate the entire blockchain
        
        Returns:
            True if chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Validate current block
            if not current_block.is_valid():
                print(f"Block {i} is invalid")
                return False
            
            # Check if hash matches
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {i} hash mismatch")
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"Block {i} previous hash mismatch")
                return False
            
            # Check proof-of-work
            if not current_block.hash.startswith('0' * self.difficulty):
                print(f"Block {i} doesn't meet difficulty requirement")
                return False
        
        return True
    
    def get_balance(self, address: str) -> float:
        """
        Get the balance of an address
        
        Args:
            address: Address to check
            
        Returns:
            Current balance
        """
        balance = 0.0
        
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                if transaction.recipient == address:
                    balance += transaction.amount
        
        return balance
    
    def get_block_by_index(self, index: int) -> Optional[Block]:
        """
        Get a block by its index
        
        Args:
            index: Block index
            
        Returns:
            Block if found, None otherwise
        """
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get blockchain statistics
        
        Returns:
            Dictionary containing blockchain stats
        """
        total_transactions = sum(len(block.transactions) for block in self.chain)
        
        return {
            'total_blocks': len(self.chain),
            'total_transactions': total_transactions,
            'pending_transactions': len(self.pending_transactions),
            'difficulty': self.difficulty,
            'mining_reward': self.mining_reward,
            'latest_block_hash': self.get_latest_block().hash if self.chain else None
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert blockchain to dictionary
        
        Returns:
            Dictionary representation of the blockchain
        """
        return {
            'chain': [block.to_dict() for block in self.chain],
            'pending_transactions': [tx.to_dict() for tx in self.pending_transactions],
            'difficulty': self.difficulty,
            'mining_reward': self.mining_reward
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Blockchain':
        """
        Create blockchain from dictionary
        
        Args:
            data: Dictionary containing blockchain data
            
        Returns:
            Blockchain instance
        """
        blockchain = cls(
            difficulty=data.get('difficulty', 4),
            mining_reward=data.get('mining_reward', 10.0)
        )
        
        # Clear the genesis block created in __init__
        blockchain.chain = []
        
        # Load blocks
        for block_data in data['chain']:
            block = Block.from_dict(block_data)
            blockchain.chain.append(block)
        
        # Load pending transactions
        blockchain.pending_transactions = [
            Transaction.from_dict(tx) for tx in data.get('pending_transactions', [])
        ]
        
        return blockchain
