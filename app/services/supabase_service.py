"""
Supabase Service
Handles all database operations with Supabase
"""

from supabase import create_client, Client
from typing import List, Dict, Any, Optional
import json
from ..config.settings import settings


class SupabaseService:
    """Service for interacting with Supabase database"""
    
    def __init__(self):
        """Initialize Supabase client"""
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self._ensure_tables_exist()
    
    def _ensure_tables_exist(self):
        """
        Ensure required tables exist in Supabase
        This will create tables if they don't exist
        """
        try:
            # Try to query tables to see if they exist
            self.supabase.table('blocks').select('*').limit(1).execute()
            self.supabase.table('transactions').select('*').limit(1).execute()
            print("✓ Supabase tables verified")
        except Exception as e:
            print(f"Note: Tables may need to be created. Error: {e}")
            print("Tables will be created automatically on first insert.")
    
    # ==================== BLOCK OPERATIONS ====================
    
    def save_block(self, block_data: Dict[str, Any]) -> bool:
        """
        Save a block to the database
        
        Args:
            block_data: Block data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data for insertion
            data = {
                'block_index': block_data['index'],
                'timestamp': block_data['timestamp'],
                'transactions': json.dumps(block_data['transactions']),
                'previous_hash': block_data['previous_hash'],
                'nonce': block_data['nonce'],
                'hash': block_data['hash']
            }
            
            # Insert into database
            result = self.supabase.table('blocks').insert(data).execute()
            
            # Save individual transactions
            for tx in block_data['transactions']:
                self.save_transaction(tx, block_data['index'])
            
            print(f"✓ Block {block_data['index']} saved to Supabase")
            return True
            
        except Exception as e:
            print(f"✗ Error saving block: {e}")
            return False
    
    def get_block_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a block by its index
        
        Args:
            index: Block index
            
        Returns:
            Block data or None
        """
        try:
            result = self.supabase.table('blocks')\
                .select('*')\
                .eq('block_index', index)\
                .execute()
            
            if result.data and len(result.data) > 0:
                block = result.data[0]
                # Parse transactions JSON
                block['transactions'] = json.loads(block['transactions'])
                block['index'] = block['block_index']
                return block
            
            return None
            
        except Exception as e:
            print(f"✗ Error getting block: {e}")
            return None
    
    def get_all_blocks(self) -> List[Dict[str, Any]]:
        """
        Get all blocks from the database
        
        Returns:
            List of block data
        """
        try:
            result = self.supabase.table('blocks')\
                .select('*')\
                .order('block_index')\
                .execute()
            
            blocks = []
            for block in result.data:
                # Parse transactions JSON
                block['transactions'] = json.loads(block['transactions'])
                block['index'] = block['block_index']
                blocks.append(block)
            
            return blocks
            
        except Exception as e:
            print(f"✗ Error getting blocks: {e}")
            return []
    
    def get_latest_block(self) -> Optional[Dict[str, Any]]:
        """
        Get the latest block from the database
        
        Returns:
            Latest block data or None
        """
        try:
            result = self.supabase.table('blocks')\
                .select('*')\
                .order('block_index', desc=True)\
                .limit(1)\
                .execute()
            
            if result.data and len(result.data) > 0:
                block = result.data[0]
                block['transactions'] = json.loads(block['transactions'])
                block['index'] = block['block_index']
                return block
            
            return None
            
        except Exception as e:
            print(f"✗ Error getting latest block: {e}")
            return None
    
    def delete_all_blocks(self) -> bool:
        """
        Delete all blocks (use with caution!)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.supabase.table('blocks').delete().neq('block_index', -1).execute()
            print("✓ All blocks deleted")
            return True
        except Exception as e:
            print(f"✗ Error deleting blocks: {e}")
            return False
    
    # ==================== TRANSACTION OPERATIONS ====================
    
    def save_transaction(self, tx_data: Dict[str, Any], block_index: int) -> bool:
        """
        Save a transaction to the database
        
        Args:
            tx_data: Transaction data dictionary
            block_index: Index of the block containing this transaction
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                'block_index': block_index,
                'sender': tx_data['sender'],
                'recipient': tx_data['recipient'],
                'amount': tx_data['amount'],
                'timestamp': tx_data['timestamp']
            }
            
            self.supabase.table('transactions').insert(data).execute()
            return True
            
        except Exception as e:
            print(f"✗ Error saving transaction: {e}")
            return False
    
    def get_transactions_by_block(self, block_index: int) -> List[Dict[str, Any]]:
        """
        Get all transactions in a specific block
        
        Args:
            block_index: Block index
            
        Returns:
            List of transaction data
        """
        try:
            result = self.supabase.table('transactions')\
                .select('*')\
                .eq('block_index', block_index)\
                .execute()
            
            return result.data
            
        except Exception as e:
            print(f"✗ Error getting transactions: {e}")
            return []
    
    def get_transactions_by_address(self, address: str) -> List[Dict[str, Any]]:
        """
        Get all transactions involving an address
        
        Args:
            address: Wallet address
            
        Returns:
            List of transaction data
        """
        try:
            # Get transactions where address is sender
            sent = self.supabase.table('transactions')\
                .select('*')\
                .eq('sender', address)\
                .execute()
            
            # Get transactions where address is recipient
            received = self.supabase.table('transactions')\
                .select('*')\
                .eq('recipient', address)\
                .execute()
            
            # Combine and return
            return sent.data + received.data
            
        except Exception as e:
            print(f"✗ Error getting transactions: {e}")
            return []
    
    def get_all_transactions(self) -> List[Dict[str, Any]]:
        """
        Get all transactions from the database
        
        Returns:
            List of transaction data
        """
        try:
            result = self.supabase.table('transactions')\
                .select('*')\
                .order('timestamp')\
                .execute()
            
            return result.data
            
        except Exception as e:
            print(f"✗ Error getting all transactions: {e}")
            return []
    
    # ==================== UTILITY OPERATIONS ====================
    
    def get_blockchain_stats(self) -> Dict[str, Any]:
        """
        Get blockchain statistics from database
        
        Returns:
            Statistics dictionary
        """
        try:
            # Count blocks
            blocks_result = self.supabase.table('blocks')\
                .select('*', count='exact')\
                .execute()
            
            # Count transactions
            tx_result = self.supabase.table('transactions')\
                .select('*', count='exact')\
                .execute()
            
            return {
                'total_blocks': blocks_result.count if hasattr(blocks_result, 'count') else len(blocks_result.data),
                'total_transactions': tx_result.count if hasattr(tx_result, 'count') else len(tx_result.data)
            }
            
        except Exception as e:
            print(f"✗ Error getting stats: {e}")
            return {
                'total_blocks': 0,
                'total_transactions': 0
            }


# Create global instance
supabase_service = SupabaseService()
