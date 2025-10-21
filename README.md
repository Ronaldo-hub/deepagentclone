# AI Agent Dashboard

Minimal scaffold for the AI Agent Dashboard project. See `backend/` for the
Python server and `frontend/` for UI placeholders.

Features
- Web search
- Code generation

Installation
```bash
pip install -r requirements.txt
```
# deepagentclone
# 🤖 AI Agent System - Complete Package

> **A production-ready AI agent system built entirely on free-tier infrastructure that can research, code, email, analyze data, and automate workflows 24/7.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📑 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Quick Start](#quick-start)
5. [Deployment](#deployment)
6. [Usage Examples](#usage-examples)
7. [API Reference](#api-reference)
8. [Advanced Features](#advanced-features)
9. [Cost & Scaling](#cost--scaling)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)

---

## 🎯 Overview

This is a **fully functional AI agent system** similar to Abacus.AI's DeepAgent, built using 100% free-tier services. It can:

- 🔍 **Search the web** and gather information
- 💻 **Write and debug code** in any language
- 📧 **Send emails** automatically
- 📊 **Analyze data** and create visualizations
- 🤖 **Automate workflows** on a schedule
- 🧠 **Remember conversations** using vector search
- 🔗 **Integrate with** Slack, GitHub, Jira, etc.
- 🎨 **Generate reports** and presentations

### What Makes This Special?

✅ **100% Free to Start** - Built on free tiers  
✅ **Production Ready** - Includes tests, monitoring, CI/CD  
✅ **Easy to Deploy** - One-click deployment options  
✅ **Fully Documented** - Complete guides and examples  
✅ **Scalable** - Easy upgrade path to paid tiers  

---

## ✨ Features

### Core Capabilities

| Feature | Description | Status |
|---------|-------------|--------|
| **Web Search** | DuckDuckGo integration, no API key needed | ✅ Active |
| **LLM Integration** | Groq (free), OpenRouter, or local LLMs | ✅ Active |
| **Vector Memory** | Semantic search with pgvector | ✅ Active |
| **Task Queue** | Redis-backed async processing | ✅ Active |
| **Database** | PostgreSQL via Supabase | ✅ Active |
| **Email** | SendGrid (100/day free) | ✅ Active |
| **GitHub** | Repo management, issue tracking | ✅ Active |
| **Slack** | Message posting, notifications | ✅ Active |
| **Scheduling** | Cron-based workflow automation | ✅ Active |
| **Monitoring** | Sentry error tracking | ✅ Active |

### Advanced Features

- 🧩 **Plugin System** - Extend with custom capabilities
- 🔄 **Workflow Engine** - Multi-step automated processes
- 🤝 **Multi-Agent** - Specialized agents working together
- 📈 **Analytics** - Track performance and usage
- 🔐 **Authentication** - Supabase Auth integration
- 🌐 **REST API** - FastAPI with auto-generated docs
- 📱 **React Dashboard** - Beautiful web interface

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                      │
│            (React Dashboard / API Clients)              │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│                      FastAPI Server                      │
│               (Request Routing & Auth)                   │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│                     AI Agent Core                        │
│         (Task Analysis & Orchestration)                  │
└─┬───────┬───────┬───────┬───────┬───────┬──────────────┘
  │       │       │       │       │       │
  ▼       ▼       ▼       ▼       ▼       ▼
┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
│Web │ │Code│ │Mail│ │Data│ │Git │ │Slak│  Specialized
│Srch│ │Gen │ │Send│ │Anls│ │Hub │ │ck  │  Agents
└─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘
  │      │      │      │      │      │
  └──────┴──────┴──────┴──────┴──────┘
                 │
                 ▼
    ┌─────────────────────────┐
    │   Infrastructure Layer   │
    ├─────────────────────────┤
    │ • Supabase (Database)   │
    │ • Redis (Queue)         │
    │ • Groq (LLM)            │
    │ • SendGrid (Email)      │
    │ • Railway (Hosting)     │
    └─────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Git
- Docker (optional, recommended)

### 1. Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ai-agent-system.git
cd ai-agent-system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Free API Keys

Follow the [Setup Guide](SETUP.md) to get your free API keys:

- ✅ Groq API (LLM - Free)
- ✅ Supabase (Database - 500MB free)
- ✅ SendGrid (Email - 100/day free)
- ✅ GitHub Token (Optional)
- ✅ Slack Token (Optional)

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 4. Run Locally

```bash
# Option A: With Docker (recommended)
docker-compose up

# Option B: Without Docker
redis-server  # In one terminal
uvicorn main:app --reload  # In another terminal
python worker.py  # In a third terminal
```

### 5. Test It!

```bash
# Visit interactive API docs
open http://localhost:8000/docs

# Or test via curl
curl -X POST http://localhost:8000/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! What can you do?"}'
```

---

## 🌐 Deployment

### One-Click Deploy Options

#### Railway (Recommended)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. Click button above
2. Connect your GitHub repo
3. Add environment variables
4. Deploy! ✨

#### Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

#### Fly.io
```bash
fly launch
fly deploy
```

### Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on:
- Oracle Cloud (most powerful free tier)
- Google Cloud
- AWS
- Self-hosting

---

## 💡 Usage Examples

### Example 1: Research & Report

```python
from main import AIAgent

agent = AIAgent()

result = await agent.process_request(
    "Research the latest AI developments and create a summary report"
)

print(result['report'])
```

### Example 2: Automated Workflow

```python
from advanced_features import WorkflowEngine

engine = WorkflowEngine()

workflow = {
    'name': 'daily_report',
    'steps': [
        {'name': 'search', 'description': 'Search for tech news'},
        {'name': 'analyze', 'description': 'Analyze trends'},
        {'name': 'email', 'description': 'Email summary to team'}
    ]
}

result = await engine.execute_workflow(workflow)
```

### Example 3: Code Generation

```python
result = await agent.process_request(
    "Write a Python REST API for user authentication with JWT tokens"
)

print(result['code'])
```

### Example 4: Data Analysis

```python
result = await agent.process_request(
    "Analyze this CSV data and identify trends: [upload file]"
)
```

### Example 5: GitHub Automation

```python
result = await agent.process_request(
    "Create a GitHub issue for bug: Login page crashes on mobile"
)
```

More examples in [EXAMPLES.md](EXAMPLES.md)

---

## 📚 API Reference

### REST Endpoints

#### POST /agent/chat
Send a message to the agent.

**Request:**
```json
{
  "message": "Your query here",
  "user_id": "optional_user_id",
  "context": {"optional": "context"}
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Request processed",
  "data": {...}
}
```

#### POST /workflow/execute
Execute a predefined workflow.

**Request:**
```json
{
  "workflow_name": "daily_research_report"
}
```

#### POST /workflow/schedule
Schedule a workflow to run periodically.

**Request:**
```json
{
  "workflow_name": "daily_research_report",
  "cron": "0 9 * * *"
}
```

#### GET /memory/search
Search agent memory using semantic similarity.

**Query Parameters:**
- `query`: Search query
- `limit`: Number of results (default: 5)

Full API docs: `http://localhost:8000/docs`

---

## 🔧 Advanced Features

### Custom Plugins

Create your own plugins:

```python
from advanced_features import AgentPlugin

class MyCustomPlugin(AgentPlugin):
    def __init__(self):
        super().__init__("my_plugin")
    
    async def execute(self, params: Dict) -> Dict:
        # Your custom logic here
        return {"result": "success"}

# Register plugin
plugin_manager.register_plugin(MyCustomPlugin())
```

### Workflow Scheduling

```python
scheduler = WorkflowScheduler()

# Run daily at 9 AM
await scheduler.schedule_workflow(
    'daily_report',
    '0 9 * * *'
)
```

### Multi-Agent Collaboration

```python
system = MultiAgentSystem()

result = await system.collaborate(
    "Research and analyze the AI market, then write a report"
)
```

See [ADVANCED.md](ADVANCED.md) for more.

---

## 💰 Cost & Scaling

### Free Tier Limits

| Service | Free Tier | Cost After |
|---------|-----------|------------|
| **Groq** | Rate limited | Free (beta) |
| **Supabase** | 500MB DB | $25/mo |
| **SendGrid** | 100 emails/day | $20/mo |
| **Railway** | $5 credit/mo | $5/mo |
| **Oracle Cloud** | Always free! | Pay as you go |

### Monthly Cost Estimate

- **Free tier only**: $0/month
- **Light usage**: ~$10-15/month
- **Medium usage**: ~$30-50/month
- **Heavy usage**: ~$100-200/month

### When to Upgrade?

- Database > 500MB → Upgrade Supabase
- Emails > 100/day → Upgrade SendGrid  
- 24/7 uptime needed → Paid hosting
- More reliability → Anthropic Claude API

---

## 🐛 Troubleshooting

### Common Issues

**Problem**: "Connection refused" error  
**Solution**: Make sure Redis is running
```bash
redis-cli ping  # Should return PONG
```

**Problem**: "Module not found"  
**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

**Problem**: API key errors  
**Solution**: Check your .env file
```bash
cat .env | grep API_KEY
```

**Problem**: Database connection errors  
**Solution**: Verify Supabase credentials
```bash
curl https://your-project.supabase.co/rest/v1/ \
  -H "apikey: your_key"
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more.

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_agent.py::test_web_search

# Run with coverage
pytest --cov=. --cov-report=html

# Interactive testing
python tests/test_agent.py
```

---

## 📊 Monitoring

### Built-in Monitoring

- **Sentry**: Error tracking and alerts
- **Health Checks**: `/health` endpoint
- **Metrics**: `/metrics` endpoint
- **Logs**: Structured logging to files

### External Monitoring

- **UptimeRobot**: Monitor uptime (free)
- **Grafana**: Visualize metrics (self-host free)
- **Papertrail**: Log aggregation (100MB free)

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

### Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/ai-agent-system.git

# Create branch
git checkout -b feature/amazing-feature

# Make changes and test
pytest

# Commit and push
git commit -m "Add amazing feature"
git push origin feature/amazing-feature

# Open Pull Request
```

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🌟 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Groq](https://groq.com/)
- Database by [Supabase](https://supabase.
