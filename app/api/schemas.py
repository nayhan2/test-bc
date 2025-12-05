"""
API Schemas
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class TransactionCreate(BaseModel):
    """Schema for creating a new transaction"""
    sender: str = Field(..., description="Sender address", min_length=1)
    recipient: str = Field(..., description="Recipient address", min_length=1)
    amount: float = Field(..., description="Amount to transfer", gt=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "sender": "Alice",
                "recipient": "Bob",
                "amount": 50.0
            }
        }


class TransactionResponse(BaseModel):
    """Schema for transaction response"""
    sender: str
    recipient: str
    amount: float
    timestamp: float


class BlockResponse(BaseModel):
    """Schema for block response"""
    index: int
    transactions: List[TransactionResponse]
    previous_hash: str
    timestamp: float
    nonce: int
    hash: str


class ChainResponse(BaseModel):
    """Schema for blockchain response"""
    chain: List[dict]
    length: int


class MineRequest(BaseModel):
    """Schema for mining request"""
    miner_address: str = Field(..., description="Address to receive mining reward", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "miner_address": "Miner1"
            }
        }


class StatsResponse(BaseModel):
    """Schema for statistics response"""
    total_blocks: int
    total_transactions: int
    pending_transactions: int
    difficulty: int
    mining_reward: float
    latest_block_hash: Optional[str]
    database_blocks: int
    database_transactions: int


class BalanceRequest(BaseModel):
    """Schema for balance request"""
    address: str = Field(..., description="Wallet address", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "address": "Alice"
            }
        }


class BalanceResponse(BaseModel):
    """Schema for balance response"""
    address: str
    balance: float
    transaction_count: int


class MessageResponse(BaseModel):
    """Schema for generic message response"""
    success: bool
    message: str
    data: Optional[dict] = None
