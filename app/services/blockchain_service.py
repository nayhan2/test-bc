"""
Blockchain Service
Business logic for blockchain operations
"""

from typing import List, Dict, Any, Optional
from ..models import Block, Blockchain, Transaction
from .supabase_service import supabase_service
from ..config.settings import settings


class BlockchainService:
    """Service for managing blockchain operations"""
    
    def __init__(self):
        """Initialize blockchain service"""
        self.blockchain = Blockchain(
            difficulty=settings.MINING_DIFFICULTY,
            mining_reward=settings.MINING_REWARD
        )
        self._load_from_database()
    
    def _load_from_database(self):
        """Load blockchain from Supabase database"""
        try:
            blocks = supabase_service.get_all_blocks()
            
            if blocks:
                print(f"Loading {len(blocks)} blocks from database...")
                
                # Clear current chain (including genesis block)
                self.blockchain.chain = []
                
                # Load each block
                for block_data in blocks:
                    block = Block.from_dict(block_data)
                    self.blockchain.chain.append(block)
                
                print(f"✓ Loaded {len(blocks)} blocks from Supabase")
            else:
                print("No blocks in database, using genesis block")
                # Save genesis block to database
                genesis = self.blockchain.get_latest_block()
                if genesis:
                    supabase_service.save_block(genesis.to_dict())
                    
        except Exception as e:
            print(f"✗ Error loading from database: {e}")
            print("Using fresh blockchain with genesis block")
    
    def get_chain(self) -> List[Dict[str, Any]]:
        """
        Get the entire blockchain
        
        Returns:
            List of block dictionaries
        """
        return [block.to_dict() for block in self.blockchain.chain]
    
    def get_block(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific block by index
        
        Args:
            index: Block index
            
        Returns:
            Block dictionary or None
        """
        block = self.blockchain.get_block_by_index(index)
        return block.to_dict() if block else None
    
    def add_transaction(self, sender: str, recipient: str, amount: float) -> Dict[str, Any]:
        """
        Add a new transaction to pending transactions
        
        Args:
            sender: Sender address
            recipient: Recipient address
            amount: Amount to transfer
            
        Returns:
            Result dictionary
        """
        transaction = Transaction(sender, recipient, amount)
        
        if self.blockchain.add_transaction(transaction):
            return {
                'success': True,
                'message': 'Transaction added to pending transactions',
                'transaction': transaction.to_dict(),
                'pending_count': len(self.blockchain.pending_transactions)
            }
        else:
            return {
                'success': False,
                'message': 'Invalid transaction',
                'transaction': None
            }
    
    def mine_block(self, miner_address: str) -> Dict[str, Any]:
        """
        Mine pending transactions into a new block
        
        Args:
            miner_address: Address to receive mining reward
            
        Returns:
            Result dictionary with mined block
        """
        if not self.blockchain.pending_transactions:
            return {
                'success': False,
                'message': 'No pending transactions to mine',
                'block': None
            }
        
        try:
            # Mine the block
            new_block = self.blockchain.mine_pending_transactions(miner_address)
            
            # Save to database
            supabase_service.save_block(new_block.to_dict())
            
            return {
                'success': True,
                'message': f'Block {new_block.index} mined successfully',
                'block': new_block.to_dict(),
                'reward': settings.MINING_REWARD
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error mining block: {str(e)}',
                'block': None
            }
    
    def validate_chain(self) -> Dict[str, Any]:
        """
        Validate the entire blockchain
        
        Returns:
            Validation result dictionary
        """
        is_valid = self.blockchain.is_chain_valid()
        
        return {
            'valid': is_valid,
            'message': 'Blockchain is valid' if is_valid else 'Blockchain is invalid',
            'total_blocks': len(self.blockchain.chain)
        }
    
    def get_balance(self, address: str) -> Dict[str, Any]:
        """
        Get balance for an address
        
        Args:
            address: Wallet address
            
        Returns:
            Balance information
        """
        balance = self.blockchain.get_balance(address)
        transactions = supabase_service.get_transactions_by_address(address)
        
        return {
            'address': address,
            'balance': balance,
            'transaction_count': len(transactions)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get blockchain statistics
        
        Returns:
            Statistics dictionary
        """
        stats = self.blockchain.get_stats()
        db_stats = supabase_service.get_blockchain_stats()
        
        return {
            **stats,
            'database_blocks': db_stats['total_blocks'],
            'database_transactions': db_stats['total_transactions']
        }
    
    def get_pending_transactions(self) -> List[Dict[str, Any]]:
        """
        Get all pending transactions
        
        Returns:
            List of pending transaction dictionaries
        """
        return [tx.to_dict() for tx in self.blockchain.pending_transactions]
    
    def reset_blockchain(self) -> Dict[str, Any]:
        """
        Reset blockchain to genesis block (use with caution!)
        
        Returns:
            Result dictionary
        """
        try:
            # Delete from database
            supabase_service.delete_all_blocks()
            
            # Create new blockchain
            self.blockchain = Blockchain(
                difficulty=settings.MINING_DIFFICULTY,
                mining_reward=settings.MINING_REWARD
            )
            
            # Save genesis block
            genesis = self.blockchain.get_latest_block()
            supabase_service.save_block(genesis.to_dict())
            
            return {
                'success': True,
                'message': 'Blockchain reset to genesis block'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error resetting blockchain: {str(e)}'
            }


# Create global instance
blockchain_service = BlockchainService()
