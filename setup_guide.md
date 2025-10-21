# 🤖 AI Agent System - Complete Setup Guide

## Overview
This guide will help you deploy a fully functional AI agent system using **100% free tier services**. You can upgrade to paid tiers later as your usage grows.

---

## 📋 Prerequisites

- GitHub account (free)
- Basic command line knowledge
- Text editor (VS Code recommended)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Your Free API Keys

#### 1.1 Groq API (LLM - Fastest Free Inference)
1. Go to https://console.groq.com
2. Sign up with GitHub/Google
3. Create API key
4. Copy key (starts with `gsk_`)

#### 1.2 Supabase (Database + Auth)
1. Go to https://supabase.com
2. Create new project
3. Wait for setup (~2 minutes)
4. Go to Settings → API
5. Copy:
   - `Project URL`
   - `anon public` key

#### 1.3 SendGrid (Email - 100/day free)
1. Go to https://sendgrid.com
2. Sign up for free account
3. Settings → API Keys → Create API Key
4. Copy key (starts with `SG.`)

#### 1.4 GitHub Token (Optional)
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`
4. Copy token

#### 1.5 Slack Bot (Optional)
1. Go to https://api.slack.com/apps
2. Create New App → From scratch
3. OAuth & Permissions → Install to Workspace
4. Copy Bot User OAuth Token (starts with `xoxb-`)

---

## 💻 Local Development Setup

### Step 2: Clone and Configure

```bash
# Create project directory
mkdir ai-agent-system
cd ai-agent-system

# Create necessary files
touch main.py worker.py requirements.txt .env docker-compose.yml

# Copy the backend code to main.py (from artifact above)
# Copy requirements.txt content (from artifact above)
# Copy docker-compose.yml content (from artifact above)
```

### Step 3: Configure Environment

Create `.env` file:

```bash
# LLM API
GROQ_API_KEY=gsk_your_key_here

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key

# Email (optional)
SENDGRID_API_KEY=SG.your_key_here

# GitHub (optional)
GITHUB_TOKEN=ghp_your_token_here

# Slack (optional)
SLACK_BOT_TOKEN=xoxb-your-token-here

# Redis (local)
REDIS_URL=redis://localhost:6379
```

### Step 4: Run Locally

#### Option A: With Docker (Recommended)
```bash
# Start all services
docker-compose up

# API will be available at http://localhost:8000
# Test it: http://localhost:8000/docs
```

#### Option B: Without Docker
```bash
# Install Redis (Mac)
brew install redis
brew services start redis

# Install Python dependencies
pip install -r requirements.txt

# Run API server
uvicorn main:app --reload

# In another terminal, run worker
python worker.py
```

### Step 5: Test Your Agent

```bash
# Test the API
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Research the latest AI trends and summarize"}'

# Or visit http://localhost:8000/docs for interactive API docs
```

---

## ☁️ Cloud Deployment (Free Hosting)

Choose ONE of these free hosting options:

### Option 1: Railway (Recommended - Easiest)

1. Go to https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub repo
4. Select your repository
5. Add environment variables (from your .env)
6. Deploy!

**Free Tier:** $5 credit/month, ~500 hours

### Option 2: Render

1. Go to https://render.com
2. New → Web Service
3. Connect your GitHub repo
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Create Web Service

**Free Tier:** 750 hours/month, sleeps after 15 min inactivity

### Option 3: Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
fly launch

# Deploy
fly deploy
```

**Free Tier:** 3 shared CPU VMs, 160GB transfer

### Option 4: Oracle Cloud (Most Powerful Free Tier)

1. Sign up at https://cloud.oracle.com
2. Create Compute Instance (Always Free: 4 OCPUs, 24GB RAM!)
3. SSH into instance
4. Install Docker:
```bash
sudo yum install docker
sudo systemctl start docker
```
5. Clone your repo and run docker-compose

**Free Tier:** 2 AMD VMs + 1 ARM VM (24GB RAM!), 200GB storage

---

## 🗄️ Database Setup (Supabase)

### Step 6: Initialize Database

1. Go to your Supabase project
2. SQL Editor → New Query
3. Copy and run the SQL schema from the deployment config artifact
4. This creates:
   - `agent_history` table
   - `agent_tasks` table
   - `agent_knowledge` table (with vector search)
   - Indexes for performance

---

## 🎨 Frontend Deployment

### Step 7: Deploy React Dashboard

The React dashboard (first artifact) can be hosted for free:

#### Option A: Vercel (Recommended)
```bash
# Create Next.js app
npx create-next-app@latest ai-agent-dashboard
cd ai-agent-dashboard

# Copy the React component to app/page.tsx
# Update API URL to your deployed backend

# Deploy
npx vercel
```

#### Option B: Netlify
1. Create new site from Git
2. Build command: `npm run build`
3. Publish directory: `out`
4. Deploy

#### Option C: GitHub Pages (Static)
```bash
# Build static version
npm run build
npm run export

# Deploy to GitHub Pages
npm install -g gh-pages
gh-pages -d out
```

---

## 🔧 Configuration & Customization

### Adding Custom Capabilities

Edit `main.py` to add new agent capabilities:

```python
class CustomAgent:
    """Your custom agent capability"""
    
    async def execute(self, params: Dict) -> Dict:
        # Your custom logic here
        return {"status": "success"}

# Register in AIAgent __init__
self.capabilities["custom"] = CustomAgent()
```

### Connecting Your Frontend to Backend

Update the API URL in your React component:

```javascript
const API_URL = 'https://your-backend-url.railway.app';

const response = await fetch(`${API_URL}/agent/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: input })
});
```

---

## 📊 Monitoring & Maintenance

### Free Monitoring Tools

1. **Sentry** (Error Tracking)
   - Sign up at https://sentry.io (5k errors/month free)
   - Add DSN to environment variables
   - Automatic error reporting

2. **Uptime Monitoring**
   - UptimeRobot: https://uptimerobot.com (50 monitors free)
   - Add your API URL

3. **Logs**
   - Railway/Render have built-in log viewers
   - Or use Papertrail (100MB/month free)

---

## 🚦 Usage Limits & Costs

### Free Tier Limits

| Service | Free Tier | Upgrade Cost |
|---------|-----------|--------------|
| Groq | Rate limited, generous | Free (for now) |
| Supabase | 500MB DB, 1GB transfer | $25/mo Pro |
| SendGrid | 100 emails/day | $20/mo (40k emails) |
| Railway | $5 credit/mo | $5/mo |
| Render | 750 hrs/mo | $7/mo hobby |
| Oracle Cloud | Always free tier | Pay as you go |
| GitHub Actions | 2000 min/mo | $4/mo (3000 min) |

### When to Upgrade

- **Supabase:** When you exceed 500MB or need more than 1GB transfer
- **Email:** When you need more than 100 emails/day
- **Hosting:** When you need 24/7 uptime without sleep
- **LLM:** Consider Anthropic Claude API when you need more reliability

---

## 🎯 Next Steps

### Phase 1: Basic Agent (✅ What we built)
- [x] Web search capability
- [x] LLM integration
- [x] Database storage
- [x] Task queue
- [x] API endpoints

### Phase 2: Enhanced Features (Next to build)
- [ ] User authentication (Supabase Auth)
- [ ] File upload handling
- [ ] Scheduled tasks (cron jobs)
- [ ] Webhook integrations
- [ ] Voice input/output
- [ ] Multi-agent collaboration

### Phase 3: Scale & Optimize
- [ ] Caching layer (Redis)
- [ ] Rate limiting
- [ ] Load balancing
- [ ] Vector search optimization
- [ ] Cost monitoring

---

## 🐛 Troubleshooting

### Common Issues

**1. "Connection refused" error**
```bash
# Check if Redis is running
redis-cli ping
# Should return PONG

# Check if services are up
docker-compose ps
```

**2. "Module not found" error**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**3. API key errors**
```bash
# Verify environment variables are loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GROQ_API_KEY'))"
```

**4. Database connection errors**
```bash
# Test Supabase connection
curl https://your-project.supabase.co/rest/v1/agent_history \
  -H "apikey: your_anon_key"
```

---

## 📚 Additional Resources

### Documentation
- Groq API: https://console.groq.com/docs
- Supabase: https://supabase.com/docs
- FastAPI: https://fastapi.tiangolo.com
- SendGrid: https://docs.sendgrid.com

### Community
- Discord: Join AI agent communities
- GitHub Discussions: Ask questions on your repo
- Stack Overflow: Tag with `ai-agents`, `fastapi`

---

## 🎁 Bonus: Pre-built Workflows

### Email Report Workflow
```python
# Send daily AI research reports
result = await agent.process_request(
    "Research latest AI developments and email summary to team@example.com"
)
```

### GitHub Automation
```python
# Auto-create issues from Slack messages
result = await agent.process_request(
    "Monitor #bugs Slack channel and create GitHub issues for new bugs"
)
```

### Data Analysis Pipeline
```python
# Automated data analysis
result = await agent.process_request(
    "Analyze uploaded CSV, generate insights, and post to Slack"
)
```

---

## ✅ Deployment Checklist

Before going to production:

- [ ] All API keys configured
- [ ] Database schema created
- [ ] Environment variables set on hosting platform
- [ ] Frontend deployed and connected to backend
- [ ] Error monitoring configured (Sentry)
- [ ] Uptime monitoring configured
- [ ] Rate limiting implemented
- [ ] CORS configured for your domain
- [ ] SSL/HTTPS enabled
- [ ] Backup strategy for database
- [ ] Documentation updated
- [ ] Test all agent capabilities

---

## 🎉 You're Done!

Your AI agent system is now live and running on free infrastructure!

**Test it:**
```bash
curl -X POST https://your-api.railway.app/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, agent! What can you do?"}'
```

**Next:** Start building custom workflows and watch your agent work for you 24/7!

Need help? Check the troubleshooting section or create an issue on GitHub.

---

## 💡 Pro Tips

1. **Start Small**: Deploy with just web search and database first
2. **Monitor Usage**: Check your free tier limits weekly
3. **Cache Responses**: Reduce API calls by caching common queries
4. **Use Webhooks**: More efficient than polling
5. **Document Everything**: Future you will thank present you
6. **Version Control**: Commit often, deploy confidently

Happy building! 🚀
