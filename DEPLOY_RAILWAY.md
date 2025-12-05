# 🚀 Deploy ke Railway.app - Step by Step

Railway.app adalah cara TERMUDAH untuk deploy Python backend Anda!

---

## 📋 Persiapan

### 1. Push Code ke GitHub

Jika belum, buat repository GitHub dan push code:

```bash
# Di folder c:\block-chain\backend
git init
git add .
git commit -m "Initial commit - Blockchain API"

# Buat repository di GitHub, lalu:
git remote add origin https://github.com/USERNAME/REPO-NAME.git
git branch -M main
git push -u origin main
```

---

## 🚂 Deploy ke Railway

### Step 1: Buat Akun Railway

1. Buka https://railway.app
2. Klik **"Login"**
3. Pilih **"Login with GitHub"**
4. Authorize Railway

### Step 2: Create New Project

1. Klik **"New Project"**
2. Pilih **"Deploy from GitHub repo"**
3. Pilih repository Anda (blockchain-backend)
4. Klik repository untuk deploy

### Step 3: Configure Environment Variables

Railway akan auto-detect Python. Sekarang set environment variables:

1. Klik tab **"Variables"**
2. Klik **"+ New Variable"**
3. Tambahkan satu per satu:

```
SUPABASE_URL = https://lqwtfwwcbjxzvzgcjlyo.supabase.co
```

```
SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxxd3Rmd3djYmp4enZ6Z2NqbHlvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ5MzA2MDQsImV4cCI6MjA4MDUwNjYwNH0.n7kHwIbauN_Rue0SlJhw7LGoTRbcn3CprXopW4Q6g6Q
```

```
MINING_DIFFICULTY = 4
```

```
MINING_REWARD = 10.0
```

### Step 4: Deploy!

Railway akan otomatis:

- ✅ Detect Python
- ✅ Install dependencies dari `requirements.txt`
- ✅ Run command dari `Procfile`
- ✅ Deploy aplikasi Anda

### Step 5: Get Your URL

1. Klik tab **"Settings"**
2. Scroll ke **"Domains"**
3. Klik **"Generate Domain"**
4. Anda akan dapat URL seperti: `https://blockchain-api-production.up.railway.app`

---

## ✅ Verifikasi Deployment

### Test API Anda

Buka di browser:

```
https://your-app.up.railway.app/docs
```

Atau test dengan curl:

```bash
curl https://your-app.up.railway.app/api/chain
```

---

## 🔧 Troubleshooting

### Build Failed?

**Cek Logs:**

1. Klik tab "Deployments"
2. Klik deployment yang failed
3. Lihat error message

**Common Issues:**

1. **Python version error**

   - Railway auto-detect Python version
   - Jika error, buat file `runtime.txt` dengan: `python-3.13.0`

2. **Module not found**

   - Pastikan semua dependencies ada di `requirements.txt`
   - Redeploy

3. **Port binding error**
   - Railway otomatis set `$PORT` environment variable
   - Pastikan `Procfile` menggunakan `--port $PORT`

### Redeploy

Setiap kali Anda push ke GitHub, Railway akan otomatis redeploy!

```bash
git add .
git commit -m "Update code"
git push
```

---

## 💰 Pricing

Railway menyediakan:

- **$5 free credit per month** (cukup untuk development)
- **Pay-as-you-go** setelah itu (~$5-10/month untuk small apps)

---

## 🎯 Next Steps

Setelah deploy berhasil:

1. ✅ Test semua API endpoints
2. ✅ Buat tabel di Supabase (jika belum)
3. ✅ Test create transaction → mine → validate
4. ✅ Share URL API Anda!

---

## 📱 Custom Domain (Opsional)

Jika ingin custom domain:

1. Di Railway, klik tab "Settings"
2. Scroll ke "Domains"
3. Klik "Add Custom Domain"
4. Ikuti instruksi untuk setup DNS

---

## 🔐 Security Tips

1. **Jangan commit `.env` file** (sudah di `.gitignore`)
2. **Set environment variables di Railway**, bukan hardcode
3. **Rotate Supabase keys** secara berkala
4. **Enable HTTPS** (Railway otomatis provide)

---

## 📊 Monitoring

Railway dashboard menampilkan:

- 📈 CPU & Memory usage
- 📝 Logs real-time
- 🔄 Deployment history
- 💰 Usage & billing

---

## ✨ Done!

API Anda sekarang live di internet! 🎉

**Share URL Anda:**

```
https://your-app.up.railway.app/docs
```

---

## 🆘 Need Help?

Railway documentation: https://docs.railway.app
Railway Discord: https://discord.gg/railway
