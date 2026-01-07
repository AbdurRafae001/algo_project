# 🚀 Deployment Guide - SafarPak to Streamlit Community Cloud

## 📋 Prerequisites

1. **GitHub Account** (free) - [Sign up here](https://github.com)
2. **Streamlit Account** (free) - [Sign up here](https://share.streamlit.io)

---

## 🎯 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon → **"New repository"**
3. Repository name: `safarpak` (or any name you prefer)
4. Description: "Route Planning System for Pakistan using Dijkstra's Algorithm"
5. Make it **Public** (required for free Streamlit hosting)
6. **DO NOT** initialize with README, .gitignore, or license
7. Click **"Create repository"**

### Step 2: Upload Your Code to GitHub

**Option A: Using GitHub Desktop (Easiest)**
1. Download [GitHub Desktop](https://desktop.github.com)
2. Install and sign in
3. File → Add Local Repository → Select your project folder
4. Commit all files with message: "Initial commit: SafarPak route planner"
5. Publish repository to GitHub

**Option B: Using Git Command Line**
```bash
# Navigate to your project folder
cd C:\Users\abdur\OneDrive\Desktop\algo_project

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: SafarPak route planner"

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/safarpak.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Option C: Using GitHub Web Interface**
1. On your new repository page, click **"uploading an existing file"**
2. Drag and drop all your project files:
   - `app.py`
   - `dijkstra.py`
   - `locations_data.py`
   - `data_preparation.py`
   - `pak_cities.csv`
   - `requirements.txt`
   - `README.md`
3. Scroll down, add commit message: "Initial commit"
4. Click **"Commit changes"**

### Step 3: Deploy to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in"** → Sign in with GitHub
3. Click **"New app"**
4. Fill in the form:
   - **Repository**: Select your `safarpak` repository
   - **Branch**: `main` (or `master`)
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (e.g., `safarpak`)
5. Click **"Deploy!"**

### Step 4: Wait for Deployment

- Streamlit will install dependencies from `requirements.txt`
- First deployment takes 2-3 minutes
- You'll see build logs in real-time
- Once done, your app will be live! 🎉

---

## 📁 Required Files Checklist

Make sure these files are in your GitHub repository:

✅ `app.py` - Main Streamlit application  
✅ `dijkstra.py` - Algorithm implementation  
✅ `locations_data.py` - Location database  
✅ `data_preparation.py` - Data processing script  
✅ `pak_cities.csv` - City data (required!)  
✅ `requirements.txt` - Python dependencies  
✅ `README.md` - Project documentation  

---

## ⚙️ Optional: Create `.streamlit/config.toml`

Create a folder `.streamlit` in your project root, then create `config.toml`:

```toml
[theme]
primaryColor = "#22c55e"
backgroundColor = "#0a0a0f"
secondaryBackgroundColor = "#12121a"
textColor = "#fafafa"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
```

---

## 🔧 Troubleshooting

### Issue: "Module not found"
- **Solution**: Make sure all dependencies are in `requirements.txt`
- Check that `pak_cities.csv` is uploaded to GitHub

### Issue: "FileNotFoundError: pak_cities.csv"
- **Solution**: Ensure `pak_cities.csv` is in the root directory of your repository
- The file must be committed to Git

### Issue: App is slow to load
- **Solution**: This is normal for the first load. Streamlit caches data after the first run.

### Issue: Map not displaying
- **Solution**: Check internet connection. Folium maps require internet to load tiles.

---

## 🌐 Your Live App URL

Once deployed, your app will be available at:
```
https://YOUR_USERNAME-safarpak.streamlit.app
```

Share this link on LinkedIn! 🎯

---

## 📝 Post-Deployment Checklist

- [ ] Test the app on the live URL
- [ ] Verify all features work (route finding, maps, drive mode)
- [ ] Check that `pak_cities.csv` loads correctly
- [ ] Test on mobile device (responsive design)
- [ ] Update LinkedIn post with live link!

---

## 🎉 Alternative Free Hosting Options

If Streamlit Community Cloud doesn't work, try:

1. **Railway** (railway.app) - Free tier available
2. **Render** (render.com) - Free tier for web services
3. **Fly.io** (fly.io) - Free tier available

---

**Need help?** Check Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)

