# 🚀 Free Deployment Guide - Streamlit Community Cloud

Your SafarPak app can be deployed **completely FREE** on Streamlit Community Cloud!

## ✅ Prerequisites

1. **GitHub Account** (free) - https://github.com
2. **Streamlit Account** (free) - https://share.streamlit.io

## 📋 Step-by-Step Deployment

### Step 1: Push to GitHub

1. Create a new repository on GitHub (make it **public** for free deployment)
2. Initialize git in your project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - SafarPak route planner"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to **https://share.streamlit.io**
2. Click **"Sign in"** and authorize with GitHub
3. Click **"New app"**
4. Fill in:
   - **Repository**: Select your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom name (e.g., `safarpak`)
5. Click **"Deploy"**

### Step 3: Wait for Deployment

- Streamlit will automatically:
  - Install dependencies from `requirements.txt`
  - Run your app
  - Provide a public URL like: `https://safarpak.streamlit.app`

## 🎉 That's It!

Your app will be live and accessible to anyone with the URL!

## 📝 Important Files for Deployment

Make sure these files are in your repository:

- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `dijkstra.py` - Algorithm implementation
- ✅ `data_preparation.py` - Data processing
- ✅ `locations_data.py` - Location data
- ✅ `pak_cities.csv` - Processed data (must be committed to Git)

## 🔧 Optional: Create `.streamlit/config.toml`

Create a folder `.streamlit` and add `config.toml`:

```toml
[theme]
primaryColor = "#22c55e"
backgroundColor = "#0a0a0f"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#fafafa"
font = "sans serif"
```

## 💡 Tips

- **Free tier includes**: Unlimited apps, public repos only
- **Custom domain**: Not available on free tier (but you get a `.streamlit.app` URL)
- **Auto-deploy**: Every push to main branch automatically redeploys
- **Logs**: View app logs in the Streamlit dashboard

## 🆓 Free Alternatives

If you want more control, other free options:
- **Heroku** (free tier discontinued, but alternatives exist)
- **Railway** (free tier with limits)
- **Render** (free tier available)
- **Fly.io** (free tier available)

But **Streamlit Community Cloud is the easiest and best for Streamlit apps!**

---

**Your app will be live at:** `https://YOUR_APP_NAME.streamlit.app` 🎉

