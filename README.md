# Python Blockchain with Supabase Integration

Sistem blockchain lengkap yang dibangun dengan Python, menggunakan Supabase sebagai database backend dan FastAPI untuk REST API.

## 🌟 Fitur

- ✅ **Blockchain Lengkap**: Implementasi blockchain dengan SHA-256 hashing
- ✅ **Proof of Work**: Mining dengan difficulty yang dapat disesuaikan
- ✅ **Transaction System**: Sistem transaksi yang lengkap
- ✅ **Supabase Integration**: Penyimpanan persistent di Supabase
- ✅ **REST API**: API lengkap dengan FastAPI
- ✅ **Auto-Sync**: Sinkronisasi otomatis dengan database
- ✅ **Validation**: Validasi blockchain dan transaksi

## 📁 Struktur Folder

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point FastAPI
│   ├── models/                 # Model blockchain
│   │   ├── block.py
│   │   ├── blockchain.py
│   │   └── transaction.py
│   ├── services/               # Business logic
│   │   ├── supabase_service.py
│   │   └── blockchain_service.py
│   ├── api/                    # API endpoints
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── config/                 # Konfigurasi
│   │   └── settings.py
│   └── utils/                  # Helper functions
│       └── helpers.py
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Cara Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Supabase

Kredensial Supabase sudah dikonfigurasi di `app/config/settings.py`:

- URL: https://lqwtfwwcbjxzvzgcjlyo.supabase.co
- Key: (sudah dikonfigurasi)

**Tabel akan dibuat otomatis** saat pertama kali menjalankan aplikasi.

#### Schema Tabel (Opsional - untuk referensi)

Jika ingin membuat tabel secara manual di Supabase SQL Editor:

```sql
-- Tabel Blocks
CREATE TABLE blocks (
    id BIGSERIAL PRIMARY KEY,
    block_index INTEGER UNIQUE NOT NULL,
    timestamp DOUBLE PRECISION NOT NULL,
    transactions JSONB NOT NULL,
    previous_hash TEXT NOT NULL,
    nonce INTEGER NOT NULL,
    hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabel Transactions
CREATE TABLE transactions (
    id BIGSERIAL PRIMARY KEY,
    block_index INTEGER NOT NULL,
    sender TEXT NOT NULL,
    recipient TEXT NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    timestamp DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index untuk performa
CREATE INDEX idx_blocks_index ON blocks(block_index);
CREATE INDEX idx_transactions_block ON transactions(block_index);
CREATE INDEX idx_transactions_sender ON transactions(sender);
CREATE INDEX idx_transactions_recipient ON transactions(recipient);
```

### 3. Jalankan Backend

```bash
# Dari folder backend
uvicorn app.main:app --reload
```

Atau:

```bash
# Dari folder backend
python -m uvicorn app.main:app --reload
```

Server akan berjalan di: **http://localhost:8000**

## 📚 API Documentation

Setelah server berjalan, akses dokumentasi interaktif:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Informasi Blockchain

#### `GET /api/chain`

Mendapatkan seluruh blockchain

**Response:**

```json
{
  "chain": [...],
  "length": 5
}
```

#### `GET /api/chain/validate`

Validasi integritas blockchain

**Response:**

```json
{
  "success": true,
  "message": "Blockchain is valid",
  "data": {
    "total_blocks": 5
  }
}
```

#### `GET /api/block/{index}`

Mendapatkan block spesifik berdasarkan index

**Response:**

```json
{
  "index": 1,
  "transactions": [...],
  "previous_hash": "...",
  "timestamp": 1234567890.123,
  "nonce": 12345,
  "hash": "0000abc..."
}
```

#### `GET /api/stats`

Mendapatkan statistik blockchain

**Response:**

```json
{
  "total_blocks": 5,
  "total_transactions": 10,
  "pending_transactions": 2,
  "difficulty": 4,
  "mining_reward": 10.0,
  "latest_block_hash": "0000abc...",
  "database_blocks": 5,
  "database_transactions": 10
}
```

### Transaksi

#### `POST /api/transaction`

Membuat transaksi baru

**Request Body:**

```json
{
  "sender": "Alice",
  "recipient": "Bob",
  "amount": 50.0
}
```

**Response:**

```json
{
  "success": true,
  "message": "Transaction added to pending transactions",
  "data": {
    "transaction": {...},
    "pending_count": 3
  }
}
```

#### `GET /api/transactions/pending`

Mendapatkan semua transaksi pending

**Response:**

```json
[
  {
    "sender": "Alice",
    "recipient": "Bob",
    "amount": 50.0,
    "timestamp": 1234567890.123
  }
]
```

### Mining

#### `POST /api/mine`

Mine transaksi pending menjadi block baru

**Request Body:**

```json
{
  "miner_address": "Miner1"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Block 5 mined successfully",
  "data": {
    "block": {...},
    "reward": 10.0
  }
}
```

### Balance

#### `POST /api/balance`

Cek balance alamat

**Request Body:**

```json
{
  "address": "Alice"
}
```

**Response:**

```json
{
  "address": "Alice",
  "balance": 150.0,
  "transaction_count": 5
}
```

### Utility

#### `POST /api/reset`

Reset blockchain ke genesis block (HATI-HATI!)

**Response:**

```json
{
  "success": true,
  "message": "Blockchain reset to genesis block",
  "data": null
}
```

## 💡 Contoh Penggunaan

### Menggunakan cURL

```bash
# 1. Buat transaksi
curl -X POST http://localhost:8000/api/transaction \
  -H "Content-Type: application/json" \
  -d '{"sender":"Alice","recipient":"Bob","amount":50}'

# 2. Buat transaksi lagi
curl -X POST http://localhost:8000/api/transaction \
  -H "Content-Type: application/json" \
  -d '{"sender":"Bob","recipient":"Charlie","amount":30}'

# 3. Mine block
curl -X POST http://localhost:8000/api/mine \
  -H "Content-Type: application/json" \
  -d '{"miner_address":"Miner1"}'

# 4. Lihat blockchain
curl http://localhost:8000/api/chain

# 5. Validasi blockchain
curl http://localhost:8000/api/chain/validate

# 6. Cek balance
curl -X POST http://localhost:8000/api/balance \
  -H "Content-Type: application/json" \
  -d '{"address":"Alice"}'

# 7. Lihat statistik
curl http://localhost:8000/api/stats
```

### Menggunakan Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Buat transaksi
response = requests.post(f"{BASE_URL}/transaction", json={
    "sender": "Alice",
    "recipient": "Bob",
    "amount": 50.0
})
print(response.json())

# Mine block
response = requests.post(f"{BASE_URL}/mine", json={
    "miner_address": "Miner1"
})
print(response.json())

# Lihat blockchain
response = requests.get(f"{BASE_URL}/chain")
print(response.json())
```

## ⚙️ Konfigurasi

Edit `app/config/settings.py` untuk mengubah:

- `MINING_DIFFICULTY`: Tingkat kesulitan mining (default: 4)
- `MINING_REWARD`: Reward untuk mining (default: 10.0)
- `SUPABASE_URL`: URL Supabase project
- `SUPABASE_KEY`: Supabase anon key

## 🔒 Keamanan

- ✅ SHA-256 hashing untuk block
- ✅ Proof-of-work mining
- ✅ Chain validation
- ✅ Transaction validation
- ✅ Immutable blockchain

## 📊 Cara Kerja

1. **Transaksi**: User membuat transaksi yang ditambahkan ke pending pool
2. **Mining**: Miner mengambil pending transactions dan mine block baru
3. **Proof of Work**: Block di-hash sampai memenuhi difficulty requirement
4. **Validation**: Block divalidasi sebelum ditambahkan ke chain
5. **Persistence**: Block dan transaksi disimpan ke Supabase
6. **Sync**: Saat restart, blockchain dimuat dari Supabase

## 🛠️ Troubleshooting

### Error: "No module named 'app'"

```bash
# Pastikan menjalankan dari folder backend
cd backend
python -m uvicorn app.main:app --reload
```

### Error: Supabase connection

- Pastikan URL dan Key Supabase benar
- Cek koneksi internet
- Verifikasi Supabase project masih aktif

### Mining terlalu lambat

- Kurangi `MINING_DIFFICULTY` di settings.py
- Default 4 = cukup cepat untuk development

## 📝 Lisensi

MIT License

## 👨‍💻 Developer

Blockchain system dengan Python dan Supabase integration

---

**Selamat menggunakan! 🚀**
