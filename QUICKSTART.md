# Quick Start Guide - Blockchain Backend

## 🚀 Cara Menjalankan Backend

### 1. Masuk ke Folder Backend

```bash
cd c:\block-chain\backend
```

### 2. Install Dependencies (Hanya Sekali)

```bash
pip install -r requirements.txt
```

### 3. Jalankan Server

```bash
python -m uvicorn app.main:app --reload --port 8001
```

Server akan berjalan di: **http://localhost:8001**

### 4. Akses API Documentation

Buka browser dan kunjungi:

- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

---

## 📝 Setup Supabase (Opsional)

Untuk menyimpan data secara persistent di Supabase:

1. Buka: https://lqwtfwwcbjxzvzgcjlyo.supabase.co
2. Login ke dashboard
3. Pilih **SQL Editor** di sidebar
4. Copy-paste SQL dari file `supabase_schema.sql`
5. Klik **Run** untuk membuat tabel

---

## 🧪 Test API

### Menggunakan Test Script

```bash
python test_api.py
```

### Menggunakan Browser

Buka: http://localhost:8001/docs dan coba endpoint:

1. POST `/api/transaction` - Buat transaksi
2. POST `/api/mine` - Mine block
3. GET `/api/chain` - Lihat blockchain

### Menggunakan cURL

```bash
# Buat transaksi
curl -X POST http://localhost:8001/api/transaction -H "Content-Type: application/json" -d "{\"sender\":\"Alice\",\"recipient\":\"Bob\",\"amount\":50}"

# Mine block
curl -X POST http://localhost:8001/api/mine -H "Content-Type: application/json" -d "{\"miner_address\":\"Miner1\"}"

# Lihat blockchain
curl http://localhost:8001/api/chain
```

---

## 📁 File Penting

- `app/main.py` - Entry point aplikasi
- `app/config/settings.py` - Konfigurasi (Supabase credentials, difficulty, dll)
- `README.md` - Dokumentasi lengkap
- `test_api.py` - Script untuk testing
- `supabase_schema.sql` - SQL schema untuk database

---

## ⚙️ Konfigurasi

Edit `app/config/settings.py` untuk mengubah:

- `MINING_DIFFICULTY` - Tingkat kesulitan mining (default: 4)
- `MINING_REWARD` - Reward untuk miner (default: 10.0)

---

## 🛑 Stop Server

Tekan `Ctrl+C` di terminal untuk menghentikan server.

---

## 📚 Dokumentasi Lengkap

Lihat `README.md` untuk dokumentasi lengkap dan contoh penggunaan.
