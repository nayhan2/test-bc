-- Supabase SQL Schema for Blockchain
-- Run this in Supabase SQL Editor to create tables manually (optional)
-- Tables will be created automatically by the application

-- Tabel untuk menyimpan blocks
CREATE TABLE IF NOT EXISTS blocks (
    id BIGSERIAL PRIMARY KEY,
    block_index INTEGER UNIQUE NOT NULL,
    timestamp DOUBLE PRECISION NOT NULL,
    transactions JSONB NOT NULL,
    previous_hash TEXT NOT NULL,
    nonce INTEGER NOT NULL,
    hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabel untuk menyimpan transactions
CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY,
    block_index INTEGER NOT NULL,
    sender TEXT NOT NULL,
    recipient TEXT NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    timestamp DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index untuk meningkatkan performa query
CREATE INDEX IF NOT EXISTS idx_blocks_index ON blocks(block_index);
CREATE INDEX IF NOT EXISTS idx_blocks_hash ON blocks(hash);
CREATE INDEX IF NOT EXISTS idx_transactions_block ON transactions(block_index);
CREATE INDEX IF NOT EXISTS idx_transactions_sender ON transactions(sender);
CREATE INDEX IF NOT EXISTS idx_transactions_recipient ON transactions(recipient);
CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp);

-- Comments untuk dokumentasi
COMMENT ON TABLE blocks IS 'Stores blockchain blocks';
COMMENT ON TABLE transactions IS 'Stores individual transactions';
COMMENT ON COLUMN blocks.block_index IS 'Position of block in the chain';
COMMENT ON COLUMN blocks.transactions IS 'JSON array of transactions in this block';
COMMENT ON COLUMN blocks.previous_hash IS 'Hash of the previous block';
COMMENT ON COLUMN blocks.nonce IS 'Proof-of-work nonce';
COMMENT ON COLUMN blocks.hash IS 'SHA-256 hash of this block';
