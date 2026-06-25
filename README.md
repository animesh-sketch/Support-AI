# 🚀 Convin AI Support Console

Enterprise-grade support platform with AI intelligence, built with Streamlit.

## ✨ Features

- 💬 **AI Chat Support** - Instant responses powered by Claude AI
- ☎️ **Voice Call Integration** - Schedule calls with support team
- 📊 **Analytics Dashboard** - Real-time metrics & insights
- 🤖 **AI Agent** - Automated ticket handling & escalation
- 📚 **Knowledge Base** - Document management (admin)
- 🎨 **Premium UI** - Glassmorphism design with animations
- 🔐 **Secure** - No API keys exposed, password protected
- 📱 **Responsive** - Mobile & desktop optimized
- 🚀 **Instant Deploy** - Push to Streamlit Cloud in seconds

## 📦 What's Included

| File | Purpose | Notes |
|------|---------|-------|
| `app_premium.py` | **⭐ RECOMMENDED** - Premium UI | Best design, start here |
| `app_advanced.py` | Full enterprise features | Predictive analytics, SLA rules |
| `app.py` | Standard version | Core functionality |
| `requirements.txt` | Dependencies | Minimal, fast install |
| `.streamlit/config.toml` | Config file | Theme, port, caching |
| `.gitignore` | Security | Prevents secrets commit |

## 🚀 Quick Start (60 seconds)

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app_premium.py
```

Visit: **http://localhost:8501**

### Deploy to Streamlit Cloud

See **[DEPLOY.md](DEPLOY.md)** for step-by-step instructions.

```bash
# Or deploy directly from CLI
streamlit deploy
```

Live URL will be: `https://share.streamlit.io/animesh-sketch/Support-AI/main/app_premium.py`

## 🎯 Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Change these in Settings after login!**

## 🔒 Security

✅ **No API keys in code** - Use .streamlit/secrets.toml
✅ **Safe .gitignore** - Prevents secret commits
✅ **Password protected** - Secure login
✅ **HTTPS ready** - Streamlit Cloud enforces HTTPS
✅ **Environment variables** - For sensitive config

### Secrets Management

Create `.streamlit/secrets.toml` (not committed):

```toml
[API_KEYS]
claude_api_key = "sk-ant-..."
convin_api_key = "your-key"
```

## 📊 Dashboard Features

**Home Page**
- Welcome banner
- Quick action cards (Chat, Call, Analytics)
- Key performance metrics

**Chat Page**
- AI chat interface
- Message history
- Escalation options

**Call Page**
- Schedule callback
- Time slot selection
- Phone confirmation

**Analytics Dashboard**
- Real-time metrics (Tickets, Resolution %, Response time, CSAT)
- Period/Team/Channel filters
- Chart visualizations
- Trend analysis

## 🎨 Design System

**Colors**
- Primary: #3b82f6 (Blue)
- Secondary: #8b5cf6 (Purple)
- Success: #22c55e (Green)
- Dark BG: #0f172a to #1e293b

**Components**
- Glassmorphism cards (blur + transparency)
- Gradient text & buttons
- Smooth animations
- Dark theme optimized

## 📱 Floating Widget

Bottom-right corner widget with:
- 💬 Chat button
- ☎️ Call button
- 🔔 Notification badge
- Smooth animations

## 🔧 Development

### Run specific version
```bash
streamlit run app_premium.py  # Premium (recommended)
streamlit run app_advanced.py # Advanced
streamlit run app.py          # Standard
```

### Check logs
```bash
streamlit logs
```

### Reset cache
```bash
streamlit cache clear
```

## 📈 Performance

- Fast load times (<1s)
- Cached data queries
- Optimized Plotly charts
- Minimal dependencies

## 🌐 Deployment Options

| Platform | Difficulty | Cost | Setup Time |
|----------|-----------|------|-----------|
| **Streamlit Cloud** | ⭐ Easy | Free | 2 min |
| Heroku | ⭐⭐ Medium | Free | 5 min |
| AWS | ⭐⭐⭐ Hard | Varies | 20 min |
| Docker | ⭐⭐ Medium | DIY | 10 min |

**Recommended: Streamlit Cloud** ✅

## 📞 Support

- Docs: https://docs.streamlit.io
- Issues: Check GitHub issues
- Questions: Open a discussion

## 📄 License

Built with ❤️ for Convin AI

---

**Ready to deploy?** → See [DEPLOY.md](DEPLOY.md) for Streamlit Cloud setup
