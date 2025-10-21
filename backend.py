# AI Agent System - Backend Architecture
# This is the main agent controller that orchestrates all capabilities

import os
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

# ============================================================================
# CONFIGURATION - Update these with your free tier credentials
# ============================================================================

class Config:
    # LLM API (Choose one - all have free tiers)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Free tier: https://groq.com
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")  # Free tier
    
    # Database - Supabase (Free tier: 500MB, 1GB transfer)
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    
    # Email - SendGrid (Free: 100 emails/day)
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    
    # GitHub (Free)
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    
    # Slack (Free tier)
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
    
    # Redis for queue (Self-hosted or Upstash free tier)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# ============================================================================
# AGENT CORE - Main orchestration logic
# ============================================================================

class TaskType(Enum):
    RESEARCH = "research"
    CODE_GENERATION = "code_generation"
    EMAIL = "email"
    DATA_ANALYSIS = "data_analysis"
    WEB_SEARCH = "web_search"
    GITHUB = "github"
    SLACK = "slack"
    REPORT_GENERATION = "report_generation"

@dataclass
class AgentTask:
    id: str
    type: TaskType
    description: str
    status: str = "pending"
    result: Optional[Dict] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

class AIAgent:
    """Main AI Agent that orchestrates all capabilities"""
    
    def __init__(self):
        self.config = Config()
        self.task_queue = []
        self.capabilities = {
            "web_search": WebSearchAgent(),
            "code_gen": CodeGenerationAgent(),
            "email": EmailAgent(),
            "database": DatabaseAgent(),
            "github": GitHubAgent(),
            "slack": SlackAgent(),
            "research": ResearchAgent(),
        }
    
    async def process_request(self, user_input: str) -> Dict:
        """
        Main entry point - analyzes user request and routes to appropriate agents
        """
        print(f"Processing request: {user_input}")
        
        # Step 1: Analyze the request using LLM
        analysis = await self._analyze_request(user_input)
        
        # Step 2: Break down into tasks
        tasks = self._create_tasks(analysis)
        
        # Step 3: Execute tasks
        results = await self._execute_tasks(tasks)
        
        # Step 4: Synthesize response
        final_response = await self._synthesize_response(results)
        
        return final_response
    
    async def _analyze_request(self, user_input: str) -> Dict:
        """Use LLM to understand what the user wants"""
        prompt = f"""Analyze this user request and determine what actions to take:
        
User Request: {user_input}

Respond in JSON format with:
- intent: primary goal (research, code, email, data_analysis, etc.)
- tasks: list of specific tasks to accomplish
- context: any relevant context or constraints
"""
        
        # Call LLM (using Groq as example - free tier)
        response = await self._call_llm(prompt)
        return json.loads(response)
    
    async def _call_llm(self, prompt: str) -> str:
        """
        Call LLM API - supports multiple providers with free tiers
        """
        # Example using Groq (fastest free inference)
        try:
            from groq import Groq
            client = Groq(api_key=self.config.GROQ_API_KEY)
            
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",  # Free tier
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            
            return completion.choices[0].message.content
        
        except Exception as e:
            print(f"LLM Error: {e}")
            # Fallback to simple pattern matching if API fails
            return self._fallback_analysis(prompt)
    
    def _fallback_analysis(self, prompt: str) -> str:
        """Simple pattern matching fallback"""
        lower_prompt = prompt.lower()
        
        if "research" in lower_prompt or "find" in lower_prompt:
            return '{"intent": "research", "tasks": ["web_search", "synthesize"]}'
        elif "code" in lower_prompt or "build" in lower_prompt:
            return '{"intent": "code", "tasks": ["code_generation"]}'
        elif "email" in lower_prompt:
            return '{"intent": "email", "tasks": ["draft_email", "send_email"]}'
        else:
            return '{"intent": "general", "tasks": ["process"]}'
    
    def _create_tasks(self, analysis: Dict) -> List[AgentTask]:
        """Convert analysis into executable tasks"""
        tasks = []
        intent = analysis.get("intent", "general")
        
        for task_name in analysis.get("tasks", []):
            task = AgentTask(
                id=f"{intent}_{len(tasks)}",
                type=TaskType(task_name) if task_name in [t.value for t in TaskType] else TaskType.RESEARCH,
                description=f"Execute {task_name}"
            )
            tasks.append(task)
        
        return tasks
    
    async def _execute_tasks(self, tasks: List[AgentTask]) -> List[Dict]:
        """Execute all tasks (can be parallelized)"""
        results = []
        
        for task in tasks:
            try:
                if task.type == TaskType.WEB_SEARCH:
                    result = await self.capabilities["web_search"].search(task.description)
                elif task.type == TaskType.CODE_GENERATION:
                    result = await self.capabilities["code_gen"].generate(task.description)
                elif task.type == TaskType.EMAIL:
                    result = await self.capabilities["email"].send(task.description)
                elif task.type == TaskType.DATA_ANALYSIS:
                    result = await self.capabilities["database"].query(task.description)
                else:
                    result = {"status": "completed", "message": f"Processed {task.type.value}"}
                
                task.status = "completed"
                task.result = result
                results.append(result)
                
            except Exception as e:
                task.status = "failed"
                task.result = {"error": str(e)}
                results.append({"error": str(e)})
        
        return results
    
    async def _synthesize_response(self, results: List[Dict]) -> Dict:
        """Combine all results into a coherent response"""
        return {
            "status": "success",
            "results": results,
            "timestamp": datetime.now().isoformat(),
            "message": "Tasks completed successfully"
        }

# ============================================================================
# SPECIALIZED AGENTS - Each handles specific capabilities
# ============================================================================

class WebSearchAgent:
    """Handles web searches and data gathering"""
    
    async def search(self, query: str) -> Dict:
        """Perform web search (can use free APIs like SerpAPI free tier)"""
        try:
            # Example: Use free search API or scraping
            # For production, integrate with SerpAPI, DuckDuckGo API, etc.
            import aiohttp
            
            # DuckDuckGo has no rate limits and no API key needed
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    
                    return {
                        "status": "success",
                        "query": query,
                        "results": data.get("RelatedTopics", [])[:5],
                        "source": "DuckDuckGo"
                    }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

class CodeGenerationAgent:
    """Generates and manages code"""
    
    async def generate(self, requirements: str) -> Dict:
        """Generate code based on requirements"""
        # Use LLM to generate code
        prompt = f"""Generate production-ready code for:
{requirements}

Include error handling, comments, and best practices."""
        
        agent = AIAgent()
        code = await agent._call_llm(prompt)
        
        return {
            "status": "success",
            "code": code,
            "language": "python",  # Could be detected from requirements
        }

class EmailAgent:
    """Handles email sending via SendGrid"""
    
    async def send(self, email_data: str) -> Dict:
        """Send email using SendGrid free tier (100 emails/day)"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            # Parse email data (would come from LLM analysis)
            message = Mail(
                from_email='agent@yourdomain.com',
                to_emails='user@example.com',
                subject='AI Agent Notification',
                html_content=f'<strong>{email_data}</strong>'
            )
            
            sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
            response = sg.send(message)
            
            return {
                "status": "success",
                "status_code": response.status_code,
                "message": "Email sent successfully"
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

class DatabaseAgent:
    """Handles database operations via Supabase"""
    
    async def query(self, query_description: str) -> Dict:
        """Execute database queries using Supabase"""
        try:
            from supabase import create_client, Client
            
            supabase: Client = create_client(
                Config.SUPABASE_URL,
                Config.SUPABASE_KEY
            )
            
            # Example: Store agent conversation history
            data = supabase.table("agent_history").insert({
                "query": query_description,
                "timestamp": datetime.now().isoformat(),
                "status": "processed"
            }).execute()
            
            return {
                "status": "success",
                "data": data.data,
                "message": "Database operation completed"
            }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

class GitHubAgent:
    """Manages GitHub operations"""
    
    async def create_repo(self, repo_data: Dict) -> Dict:
        """Create GitHub repository"""
        try:
            import aiohttp
            
            headers = {
                "Authorization": f"token {Config.GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.github.com/user/repos",
                    headers=headers,
                    json=repo_data
                ) as response:
                    data = await response.json()
                    
                    return {
                        "status": "success",
                        "repo_url": data.get("html_url"),
                        "message": "Repository created"
                    }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

class SlackAgent:
    """Sends notifications to Slack"""
    
    async def post_message(self, channel: str, message: str) -> Dict:
        """Post message to Slack channel"""
        try:
            import aiohttp
            
            headers = {
                "Authorization": f"Bearer {Config.SLACK_BOT_TOKEN}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "channel": channel,
                "text": message
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://slack.com/api/chat.postMessage",
                    headers=headers,
                    json=payload
                ) as response:
                    data = await response.json()
                    
                    return {
                        "status": "success" if data.get("ok") else "error",
                        "message": "Message posted to Slack"
                    }
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

class ResearchAgent:
    """Performs deep research by combining multiple searches"""
    
    async def research(self, topic: str) -> Dict:
        """Conduct comprehensive research on a topic"""
        search_agent = WebSearchAgent()
        
        # Perform multiple related searches
        searches = [
            f"{topic} overview",
            f"{topic} latest developments",
            f"{topic} best practices"
        ]
        
        results = []
        for query in searches:
            result = await search_agent.search(query)
            results.append(result)
        
        # Use LLM to synthesize findings
        agent = AIAgent()
        synthesis_prompt = f"""Synthesize these research findings into a comprehensive report:
{json.dumps(results, indent=2)}

Create a structured report with:
1. Executive Summary
2. Key Findings
3. Detailed Analysis
4. Recommendations"""
        
        report = await agent._call_llm(synthesis_prompt)
        
        return {
            "status": "success",
            "topic": topic,
            "report": report,
            "sources": len(results)
        }

# ============================================================================
# TASK QUEUE - Background job processing
# ============================================================================

class TaskQueue:
    """Redis-backed task queue for async processing"""
    
    def __init__(self):
        import redis
        self.redis_client = redis.from_url(Config.REDIS_URL)
    
    async def enqueue(self, task: Dict):
        """Add task to queue"""
        self.redis_client.lpush("agent_tasks", json.dumps(task))
    
    async def process_queue(self):
        """Worker process to handle queued tasks"""
        agent = AIAgent()
        
        while True:
            task_json = self.redis_client.brpop("agent_tasks", timeout=1)
            
            if task_json:
                task = json.loads(task_json[1])
                result = await agent.process_request(task["request"])
                
                # Store result
                self.redis_client.set(
                    f"result:{task['id']}", 
                    json.dumps(result),
                    ex=3600  # Expire after 1 hour
                )

# ============================================================================
# API SERVER - FastAPI endpoint (optional)
# ============================================================================

# The FastAPI endpoints are optional for running tests locally. If `fastapi`
# is not installed in the environment we skip creating the app so the module
# can be imported by tests that don't require the HTTP server.
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel

    app = FastAPI(title="AI Agent System", version="1.0.0")

    # Enable CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure for your domain in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class AgentRequest(BaseModel):
        message: str
        user_id: Optional[str] = None
        context: Optional[Dict] = None

    class AgentResponse(BaseModel):
        status: str
        message: str
        data: Optional[Dict] = None
        task_id: Optional[str] = None

    @app.get("/")
    async def root():
        """Health check endpoint"""
        return {
            "status": "online",
            "version": "1.0.0",
            "capabilities": [
                "web_search",
                "code_generation",
                "email",
                "database",
                "github",
                "slack",
                "research"
            ]
        }

    @app.post("/agent/chat", response_model=AgentResponse)
    async def chat_with_agent(request: AgentRequest):
        """Main endpoint to interact with the agent"""
        try:
            agent = AIAgent()
            result = await agent.process_request(request.message)

            return AgentResponse(
                status="success",
                message="Request processed successfully",
                data=result
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/agent/task", response_model=AgentResponse)
    async def create_task(request: AgentRequest):
        """Create async task (for long-running operations)"""
        try:
            import uuid
            task_id = str(uuid.uuid4())

            queue = TaskQueue()
            await queue.enqueue({
                "id": task_id,
                "request": request.message,
                "user_id": request.user_id,
                "context": request.context
            })

            return AgentResponse(
                status="queued",
                message="Task queued for processing",
                task_id=task_id
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/agent/task/{task_id}")
    async def get_task_status(task_id: str):
        """Check status of async task"""
        try:
            queue = TaskQueue()
            result = queue.redis_client.get(f"result:{task_id}")

            if result:
                return json.loads(result)
            else:
                return {"status": "processing", "task_id": task_id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
except ImportError:
    app = None
    # FastAPI or Pydantic not installed; API endpoints are disabled in this env.

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example of how to use the agent"""
    
    agent = AIAgent()
    
    # Example 1: Research task
    print("\n=== Research Task ===")
    result = await agent.process_request(
        "Research the latest trends in AI agents and create a summary report"
    )
    print(json.dumps(result, indent=2))
    
    # Example 2: Code generation
    print("\n=== Code Generation Task ===")
    result = await agent.process_request(
        "Write a Python script to scrape website data and save to CSV"
    )
    print(json.dumps(result, indent=2))
    
    # Example 3: Email task
    print("\n=== Email Task ===")
    result = await agent.process_request(
        "Send an email to the team about today's research findings"
    )
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    # For testing the agent directly
    asyncio.run(main())
