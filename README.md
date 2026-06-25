# 🎯 Anamika - Enterprise Support Widget

Premium floating support widget with Chat, Voice, Knowledge Base, Admin Panel, and Advanced Analytics. Built with Streamlit × Convin AI.

## ✨ Features

### 🎯 Core Widget
- **Floating Widget** - Bottom-right corner, always accessible
- **Notification Badge** - Unread message counter
- **Premium Design** - Glassmorphism with smooth animations

### 💬 Chat Support
- **AI-Powered** - Claude AI instant responses
- **Human Escalation** - Seamless agent transfer
- **Full History** - Persistent conversation logs

### ☎️ Voice Integration
- **Convin Sense API** - Crystal-clear voice calls
- **Call Scheduling** - Callback requests with time slots
- **Call Analytics** - Success rates & duration tracking

### 📚 Knowledge Base (Admin Only)
- **Multi-format Support** - PDF, DOC, DOCX, TXT, CSV, XLS, XLSX, PPT, PPTX, URLs
- **Smart Retrieval** - AI references KB before responding
- **Usage Analytics** - Track deflection rates & popular articles

### 📊 Advanced Analytics
- **Real-time Dashboard** - Conversations, resolution rates, CSAT
- **Chat Intelligence** - Message volume, response times, sentiment
- **Voice Intelligence** - Call success rates, duration, connected calls
- **KB Analytics** - Article views, deflection metrics, hit rates
- **Agent Performance** - Handling time, satisfaction scores, FCR

### 🔐 Admin Panel (Protected)
- **Knowledge Base Management** - Upload, edit, version documents
- **Voice Configuration** - Convin Sense API setup & controls
- **Agent Routing** - Assign agents with skills & availability
- **Escalation Rules** - Smart routing based on triggers
- **Business Hours** - Configure availability & after-hours messaging
- **Bot Controls** - Confidence thresholds, conversation limits, timeouts

### ✨ Enterprise Features
- **Auto-Escalation** - Confidence-based intelligent routing
- **Conversation Logging** - Audit trail & compliance
- **Feedback Collection** - CSAT surveys & sentiment tracking
- **Multi-agent Routing** - Load balancing & skill-based assignment
- **SLA Tracking** - Response & resolution time monitoring

## 📦 What's Included

| File | Purpose |
|------|---------|
| **app.py** | ⭐ **ANAMIKA** - Main floating widget with all features |
| `app_premium.py` | Premium UI version (archived) |
| `app_advanced.py` | Advanced analytics version (archived) |
| `requirements.txt` | Dependencies (streamlit, pandas, plotly) |
| `.streamlit/config.toml` | Streamlit theme & config |
| `.gitignore` | Security (no secrets committed) |

**Run the main app.py to launch Anamika!**

## 🚀 Quick Start (60 seconds)

### Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run Anamika widget
streamlit run app.py
```

Visit: **http://localhost:8501**

The **🎯 floating widget** is in the bottom-right corner!

### Deploy to Streamlit Cloud

```bash
git push origin main
# Then go to https://streamlit.io/cloud and deploy
```

Live at: `https://share.streamlit.io/animesh-sketch/Support-AI/main/app.py`

## 🔐 Admin Credentials

**Access Admin Panel:**
- Click **Home** → **🔐 Admin**
- Password: `admin@anamika`

⚠️ **Change admin password in production!**

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
