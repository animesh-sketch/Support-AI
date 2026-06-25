# 🚀 Streamlit Cloud Deployment Guide

## Quick Deploy (1 minute)

### Step 1: Create Streamlit Account
Go to: **https://streamlit.io/cloud**
Sign up with GitHub

### Step 2: Deploy This App
1. Click **"New app"**
2. Select repository: `animesh-sketch/Support-AI`
3. Branch: `main`
4. Main file path: `app_premium.py`
5. Click **"Deploy"** ✅

### Step 3: Share Your Live App
Your app is live at:
```
https://share.streamlit.io/[your-username]/Support-AI/main/app_premium.py
```

---

## Available Versions

### 🌟 **app_premium.py** (RECOMMENDED)
Best UI with glassmorphism, animations, premium metrics
- ⭐ Ultra-modern design system
- 🎨 Gradient text & cards
- ✨ Smooth animations
- 💬 Chat support
- ☎️ Call scheduling
- 📊 Analytics dashboard
- 🎯 Floating widget with notifications

**Deploy this one** ↑

---

### 🔧 **app_advanced.py**
Full enterprise features with advanced analytics
- 6 KPI metrics
- Advanced filtering (Period, Team, Channel, Sentiment)
- AI insights dashboard
- Performance trends
- Real-time bot monitoring
- Predictive analytics
- SLA rules & webhooks
- KB versioning

---

### 📋 **app.py**
Standard console with core features
- Dashboard, Chat, Voice, Chat Analytics
- Knowledge Base management
- Settings panel
- Real-time metrics

---

## Environment Variables (Optional)

Create `secrets.toml` in `.streamlit/` folder:

```toml
[API_KEYS]
claude_api_key = "sk-..."  # Only if using Claude API
convin_api_key = "your-key"  # Only if using Convin API
```

**NO SECRETS IN CODE** ✅

---

## Troubleshooting

### App not loading?
1. Check requirements.txt has all dependencies
2. Ensure main file path is correct
3. Check app logs in Streamlit dashboard

### Port already in use (local)?
```bash
streamlit run app_premium.py --server.port 8502
```

### Cache issues?
Streamlit > Settings > Clear cache

---

## Performance Tips

✅ **Caching Results**
```python
@st.cache_data
def fetch_data():
    return ...
```

✅ **Lazy Load Images**
Use URL instead of local files

✅ **Pagination**
Load data in chunks

---

## What's Deployed

```
Repository: https://github.com/animesh-sketch/Support-AI
├── app_premium.py        ← Premium UI (RECOMMENDED)
├── app_advanced.py       ← Full enterprise features
├── app.py                ← Standard version
├── requirements.txt      ← Dependencies
├── .gitignore            ← Prevents secret commits
├── README.md             ← Documentation
└── DEPLOY.md             ← This file
```

---

## Security Checklist

✅ No API keys in code
✅ Secrets in .streamlit/secrets.toml (local only)
✅ GitHub secrets for cloud (if needed)
✅ Password-protected pages
✅ HTTPS enforced
✅ Safe .gitignore

---

## Next Steps

1. Deploy app_premium.py to Streamlit Cloud
2. Share URL with team
3. Gather feedback
4. Iterate & redeploy (automatic on GitHub push)

Happy deploying! 🎉
