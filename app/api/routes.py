"""
API Routes
REST API endpoints for blockchain operations
"""

from fastapi import APIRouter, HTTPException, status
from typing import List
from .schemas import (
    TransactionCreate,
    TransactionResponse,
    BlockResponse,
    ChainResponse,
    MineRequest,
    StatsResponse,
    BalanceRequest,
    BalanceResponse,
    MessageResponse
)
from ..services.blockchain_service import blockchain_service

# Create router
router = APIRouter(prefix="/api", tags=["blockchain"])


@router.get("/", response_model=MessageResponse)
async def root():
    """API root endpoint"""
    return {
        "success": True,
        "message": "Blockchain API is running",
        "data": {
            "version": "1.0.0",
            "endpoints": [
                "GET /api/chain - Get entire blockchain",
                "GET /api/chain/validate - Validate blockchain",
                "GET /api/block/{index} - Get specific block",
                "POST /api/transaction - Create new transaction",
                "GET /api/transactions/pending - Get pending transactions",
                "POST /api/mine - Mine pending transactions",
                "GET /api/stats - Get blockchain statistics",
                "POST /api/balance - Get address balance",
                "POST /api/reset - Reset blockchain (caution!)"
            ]
        }
    }


@router.get("/chain", response_model=ChainResponse)
async def get_chain():
    """Get the entire blockchain"""
    chain = blockchain_service.get_chain()
    return {
        "chain": chain,
        "length": len(chain)
    }


@router.get("/chain/validate", response_model=MessageResponse)
async def validate_chain():
    """Validate the blockchain"""
    result = blockchain_service.validate_chain()
    return {
        "success": result['valid'],
        "message": result['message'],
        "data": {
            "total_blocks": result['total_blocks']
        }
    }


@router.get("/block/{index}", response_model=dict)
async def get_block(index: int):
    """Get a specific block by index"""
    block = blockchain_service.get_block(index)
    
    if block is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Block with index {index} not found"
        )
    
    return block


@router.post("/transaction", response_model=MessageResponse)
async def create_transaction(transaction: TransactionCreate):
    """Create a new transaction"""
    result = blockchain_service.add_transaction(
        sender=transaction.sender,
        recipient=transaction.recipient,
        amount=transaction.amount
    )
    
    if not result['success']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result['message']
        )
    
    return {
        "success": True,
        "message": result['message'],
        "data": {
            "transaction": result['transaction'],
            "pending_count": result['pending_count']
        }
    }


@router.get("/transactions/pending", response_model=List[dict])
async def get_pending_transactions():
    """Get all pending transactions"""
    return blockchain_service.get_pending_transactions()


@router.post("/mine", response_model=MessageResponse)
async def mine_block(request: MineRequest):
    """Mine pending transactions into a new block"""
    result = blockchain_service.mine_block(request.miner_address)
    
    if not result['success']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result['message']
        )
    
    return {
        "success": True,
        "message": result['message'],
        "data": {
            "block": result['block'],
            "reward": result['reward']
        }
    }


@router.get("/stats", response_model=dict)
async def get_stats():
    """Get blockchain statistics"""
    return blockchain_service.get_stats()


@router.post("/balance", response_model=BalanceResponse)
async def get_balance(request: BalanceRequest):
    """Get balance for an address"""
    result = blockchain_service.get_balance(request.address)
    return result


@router.post("/reset", response_model=MessageResponse)
async def reset_blockchain():
    """
    Reset blockchain to genesis block
    WARNING: This will delete all blocks and transactions!
    """
    result = blockchain_service.reset_blockchain()
    
    if not result['success']:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result['message']
        )
    
    return {
        "success": True,
        "message": result['message'],
        "data": None
    }
