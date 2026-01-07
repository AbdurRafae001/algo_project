# ⚡ Quick Deploy Checklist

## ✅ Pre-Deployment Checklist

Before deploying, ensure:

- [x] `pak_cities.csv` exists in project root
- [x] `requirements.txt` has all dependencies
- [x] All Python files are present (`app.py`, `dijkstra.py`, `locations_data.py`)
- [x] Test locally: `streamlit run app.py` works

## 🚀 Fastest Deployment Path

### 1. GitHub Setup (5 minutes)
```
1. Create account: github.com
2. New repository → Name: "safarpak" → Public → Create
3. Upload files via web interface OR use GitHub Desktop
```

### 2. Streamlit Deploy (2 minutes)
```
1. Go to: share.streamlit.io
2. Sign in with GitHub
3. New app → Select repository → Main file: app.py → Deploy
```

### 3. Done! 🎉
Your app will be live at: `https://YOUR_USERNAME-safarpak.streamlit.app`

## 📦 Files to Upload

**Required:**
- ✅ `app.py`
- ✅ `dijkstra.py`
- ✅ `locations_data.py`
- ✅ `pak_cities.csv` ← **CRITICAL!**
- ✅ `requirements.txt`

**Optional:**
- `README.md`
- `data_preparation.py`
- `.gitignore`

**Don't upload:**
- ❌ `__pycache__/`
- ❌ `simplemaps_worldcities_basicv1.901/` (too large)
- ❌ `.pdf` files

## 🔗 Share Your App

Once deployed, update your LinkedIn post with:
```
🌐 Try it live: https://YOUR_USERNAME-safarpak.streamlit.app
```

---

**Need detailed instructions?** See `DEPLOYMENT_GUIDE.md`

