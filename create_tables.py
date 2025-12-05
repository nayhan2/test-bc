"""
Script untuk membuat tabel Supabase
Jalankan script ini untuk membuat tabel secara otomatis
"""

from supabase import create_client

# Konfigurasi Supabase
SUPABASE_URL = "https://lqwtfwwcbjxzvzgcjlyo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxxd3Rmd3djYmp4enZ6Z2NqbHlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5MzA2MDQsImV4cCI6MjA4MDUwNjYwNH0.n7kHwIbauN_Rue0SlJhw7LGoTRbcn3CprXopW4Q6g6Q"

# SQL untuk membuat tabel
CREATE_TABLES_SQL = """
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
"""

def create_tables():
    """Membuat tabel di Supabase"""
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        print("=" * 60)
        print("📊 Membuat tabel di Supabase...")
        print("=" * 60)
        
        # Note: Supabase Python client tidak support SQL execution
        # Tabel harus dibuat melalui Supabase Dashboard SQL Editor
        
        print("\n⚠️  PERHATIAN:")
        print("Tabel harus dibuat melalui Supabase Dashboard")
        print("\nLangkah-langkah:")
        print("1. Buka: https://lqwtfwwcbjxzvzgcjlyo.supabase.co")
        print("2. Pilih 'SQL Editor' di sidebar")
        print("3. Copy-paste SQL dari file 'supabase_schema.sql'")
        print("4. Klik 'Run' untuk execute SQL")
        print("\nAtau tabel akan dibuat otomatis saat insert pertama kali")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_tables()
