# Deployment Guide - Python Blockchain Backend

## ⚠️ Penting: Vercel & Python

**Vercel TIDAK mendukung Python backend secara native.** Vercel dirancang untuk:

- Node.js/JavaScript
- Next.js, React, Vue
- Serverless Functions (Node.js)

Untuk deploy backend Python FastAPI, gunakan salah satu platform berikut:

---

## 🚀 Opsi Deployment (Recommended)

### 1. **Railway.app** ⭐ (PALING MUDAH)

Railway adalah platform yang sangat mudah untuk deploy Python apps.

#### Langkah-langkah:

**A. Persiapan File**

Buat file `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Buat file `Procfile`:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**B. Deploy ke Railway**

1. Buka https://railway.app
2. Sign up/Login dengan GitHub
3. Klik "New Project"
4. Pilih "Deploy from GitHub repo"
5. Connect repository Anda
6. Railway akan auto-detect Python dan deploy

**C. Set Environment Variables**

Di Railway dashboard:

- Klik project → Variables
- Tambahkan:
  ```
  SUPABASE_URL=https://lqwtfwwcbjxzvzgcjlyo.supabase.co
  SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
  ```

**D. Deploy!**

Railway akan otomatis build dan deploy. Anda akan dapat URL seperti:
`https://your-app.railway.app`

---

### 2. **Render.com** ⭐ (GRATIS)

Render menyediakan free tier untuk Python apps.

#### Langkah-langkah:

**A. Persiapan File**

Buat file `render.yaml`:

```yaml
services:
  - type: web
    name: blockchain-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: SUPABASE_URL
        value: https://lqwtfwwcbjxzvzgcjlyo.supabase.co
      - key: SUPABASE_KEY
        value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**B. Deploy ke Render**

1. Buka https://render.com
2. Sign up/Login
3. Klik "New +" → "Web Service"
4. Connect GitHub repository
5. Pilih "Python" environment
6. Build Command: `pip install -r requirements.txt`
7. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
8. Klik "Create Web Service"

URL: `https://your-app.onrender.com`

---

### 3. **Heroku** (Berbayar)

Heroku dahulu gratis, sekarang berbayar mulai $5/bulan.

#### Langkah-langkah:

**A. Install Heroku CLI**

```bash
# Download dari https://devcenter.heroku.com/articles/heroku-cli
```

**B. Persiapan File**

Buat file `Procfile`:

```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Buat file `runtime.txt`:

```
python-3.13.0
```

**C. Deploy**

```bash
# Login
heroku login

# Create app
heroku create blockchain-api

# Set environment variables
heroku config:set SUPABASE_URL=https://lqwtfwwcbjxzvzgcjlyo.supabase.co
heroku config:set SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Deploy
git push heroku main
```

URL: `https://blockchain-api.herokuapp.com`

---

### 4. **Google Cloud Run** (Pay-as-you-go)

Serverless container platform dari Google.

#### Langkah-langkah:

**A. Buat Dockerfile**

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**B. Deploy**

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Deploy
gcloud run deploy blockchain-api \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated
```

---

### 5. **DigitalOcean App Platform**

Simple dan mudah digunakan.

#### Langkah-langkah:

1. Buka https://cloud.digitalocean.com/apps
2. Klik "Create App"
3. Connect GitHub repository
4. Pilih branch
5. DigitalOcean auto-detect Python
6. Set environment variables
7. Deploy!

Harga: Mulai dari $5/bulan

---

## 📦 File yang Perlu Dibuat

Untuk semua platform di atas, pastikan Anda punya:

### ✅ `requirements.txt` (Sudah ada)

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
supabase==2.3.0
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
```

### ✅ `.gitignore` (Sudah ada)

### ⚠️ Update `settings.py`

Ubah `app/config/settings.py` untuk membaca dari environment variables:

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "https://lqwtfwwcbjxzvzgcjlyo.supabase.co")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

    # Blockchain Configuration
    MINING_DIFFICULTY: int = int(os.getenv("MINING_DIFFICULTY", "4"))
    MINING_REWARD: float = float(os.getenv("MINING_REWARD", "10.0"))

    # API Configuration
    API_TITLE: str = "Blockchain API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "A complete blockchain system with Supabase integration"

    # CORS Configuration
    CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## 🎯 Rekomendasi Saya

### Untuk Development/Testing:

✅ **Railway.app** - Paling mudah, auto-deploy dari GitHub

### Untuk Production:

✅ **Render.com** - Free tier tersedia, reliable
✅ **DigitalOcean** - Lebih kontrol, harga terjangkau

### Jangan Gunakan:

❌ **Vercel** - Tidak support Python backend

---

## 🔐 Environment Variables yang Dibutuhkan

Semua platform membutuhkan environment variables ini:

```env
SUPABASE_URL=https://lqwtfwwcbjxzvzgcjlyo.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxxd3Rmd3djYmp4enZ6Z2NqbHlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5MzA2MDQsImV4cCI6MjA4MDUwNjYwNH0.n7kHwIbauN_Rue0SlJhw7LGoTRbcn3CprXopW4Q6g6Q
MINING_DIFFICULTY=4
MINING_REWARD=10.0
```

---

## 📝 Checklist Sebelum Deploy

- [ ] Push code ke GitHub repository
- [ ] Pastikan `requirements.txt` lengkap
- [ ] Buat file deployment (Procfile/railway.json/dll)
- [ ] Update `settings.py` untuk baca environment variables
- [ ] Test locally dengan `uvicorn app.main:app`
- [ ] Siapkan environment variables
- [ ] Deploy!

---

## 🆘 Butuh Bantuan?

Pilih platform yang Anda ingin gunakan, dan saya akan bantu setup lengkapnya!

**Platform mana yang Anda pilih?**

1. Railway.app (Termudah)
2. Render.com (Gratis)
3. Heroku (Berbayar)
4. Google Cloud Run
5. DigitalOcean
