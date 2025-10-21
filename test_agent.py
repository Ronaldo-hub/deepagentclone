# Complete Test Suite for AI Agent System
# tests/test_agent.py

import pytest
import asyncio
from datetime import datetime
from main import AIAgent, WebSearchAgent, EmailAgent, DatabaseAgent
from advanced_features import (
    AgentMemory, WorkflowEngine, PluginManager, 
    WeatherPlugin, MultiAgentSystem
)

# ============================================================================
# MONITORING & HEALTH CHECKS
# ============================================================================

async def health_check():
    """Comprehensive system health check"""
    print("\n=== SYSTEM HEALTH CHECK ===\n")
    
    checks = {
        'API': check_api_health,
        'Database': check_database_health,
        'Redis': check_redis_health,
        'External APIs': check_external_apis,
    }
    
    results = {}
    
    for check_name, check_func in checks.items():
        try:
            status = await check_func()
            results[check_name] = status
            symbol = "✓" if status['healthy'] else "✗"
            print(f"{symbol} {check_name}: {status['message']}")
        except Exception as e:
            results[check_name] = {'healthy': False, 'message': str(e)}
            print(f"✗ {check_name}: ERROR - {e}")
    
    return results

async def check_api_health():
    """Check if main API is responsive"""
    import aiohttp
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/') as response:
                if response.status == 200:
                    return {'healthy': True, 'message': 'API is responsive'}
                else:
                    return {'healthy': False, 'message': f'Status code: {response.status}'}
    except Exception as e:
        return {'healthy': False, 'message': f'Cannot connect: {e}'}

async def check_database_health():
    """Check database connectivity"""
    try:
        from supabase import create_client
        from main import Config
        
        supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        result = supabase.table('agent_history').select('id').limit(1).execute()
        
        return {'healthy': True, 'message': 'Database connected'}
    except Exception as e:
        return {'healthy': False, 'message': f'Database error: {e}'}

async def check_redis_health():
    """Check Redis connectivity"""
    try:
        import redis
        from main import Config
        
        client = redis.from_url(Config.REDIS_URL)
        client.ping()
        
        return {'healthy': True, 'message': 'Redis connected'}
    except Exception as e:
        return {'healthy': False, 'message': f'Redis error: {e}'}

async def check_external_apis():
    """Check external API connectivity"""
    try:
        from main import Config
        
        # Check if API keys are configured
        apis = {
            'Groq': bool(Config.GROQ_API_KEY),
            'Supabase': bool(Config.SUPABASE_URL and Config.SUPABASE_KEY),
            'SendGrid': bool(Config.SENDGRID_API_KEY),
        }
        
        configured = sum(apis.values())
        total = len(apis)
        
        return {
            'healthy': configured >= 2,  # At least 2 APIs should be configured
            'message': f'{configured}/{total} APIs configured',
            'details': apis
        }
    except Exception as e:
        return {'healthy': False, 'message': f'Config error: {e}'}

# ============================================================================
# DEMO SCENARIOS
# ============================================================================

async def demo_complete_system():
    """Comprehensive demo of all system capabilities"""
    print("\n" + "="*60)
    print("COMPLETE SYSTEM DEMO")
    print("="*60 + "\n")
    
    agent = AIAgent()
    
    # Demo 1: Basic conversation
    print("📝 Demo 1: Basic Conversation")
    print("-" * 40)
    result = await agent.process_request("Hello! What can you do?")
    print(f"Response: {result.get('message', 'N/A')}\n")
    
    # Demo 2: Web search and research
    print("🔍 Demo 2: Web Search & Research")
    print("-" * 40)
    result = await agent.process_request(
        "Search for the latest news about SpaceX"
    )
    print(f"Found {len(result.get('results', []))} results\n")
    
    # Demo 3: Code generation
    print("💻 Demo 3: Code Generation")
    print("-" * 40)
    result = await agent.process_request(
        "Write a Python function to validate email addresses"
    )
    print(f"Generated code:\n{result.get('code', 'N/A')[:200]}...\n")
    
    # Demo 4: Workflow execution
    print("⚙️ Demo 4: Workflow Execution")
    print("-" * 40)
    engine = WorkflowEngine()
    workflow = {
        'name': 'demo_workflow',
        'steps': [
            {'name': 'research', 'description': 'Research AI agents'},
            {'name': 'summarize', 'description': 'Summarize findings'},
        ]
    }
    result = await engine.execute_workflow(workflow)
    print(f"Workflow status: {result['status']}\n")
    
    # Demo 5: Plugin system
    print("🔌 Demo 5: Plugin System")
    print("-" * 40)
    plugin_mgr = PluginManager()
    plugin_mgr.register_plugin(WeatherPlugin())
    result = await plugin_mgr.execute_plugin('weather', {'location': 'Tokyo'})
    print(f"Weather in {result['location']}: {result['temperature']}°C, {result['condition']}\n")
    
    # Demo 6: Memory system
    print("🧠 Demo 6: Memory System")
    print("-" * 40)
    memory = AgentMemory()
    await memory.store_memory(
        "AI agents are becoming increasingly sophisticated",
        {'topic': 'AI', 'importance': 'high'}
    )
    results = await memory.search_memory("artificial intelligence", limit=3)
    print(f"Found {len(results)} relevant memories\n")
    
    # Demo 7: Multi-agent collaboration
    print("🤝 Demo 7: Multi-Agent Collaboration")
    print("-" * 40)
    multi_system = MultiAgentSystem()
    result = await multi_system.collaborate(
        "Analyze the impact of AI on healthcare"
    )
    print(f"Collaboration complete with {len(result)} components\n")
    
    print("="*60)
    print("DEMO COMPLETE")
    print("="*60 + "\n")

# ============================================================================
# INTERACTIVE TESTING CLI
# ============================================================================

async def interactive_test_cli():
    """Interactive command-line interface for testing"""
    print("\n" + "="*60)
    print("INTERACTIVE AGENT TEST CLI")
    print("="*60)
    print("\nCommands:")
    print("  ask <query>     - Send a query to the agent")
    print("  workflow <name> - Execute a workflow")
    print("  plugin <name>   - Execute a plugin")
    print("  memory <query>  - Search agent memory")
    print("  health          - Check system health")
    print("  metrics         - Show performance metrics")
    print("  help            - Show this help")
    print("  exit            - Exit CLI")
    print("="*60 + "\n")
    
    agent = AIAgent()
    memory = AgentMemory()
    plugin_mgr = PluginManager()
    plugin_mgr.register_plugin(WeatherPlugin())
    
    while True:
        try:
            user_input = input("agent> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""
            
            if command == "exit":
                print("Goodbye!")
                break
            
            elif command == "ask":
                if not args:
                    print("Usage: ask <your question>")
                    continue
                print(f"\nProcessing: {args}")
                result = await agent.process_request(args)
                print(f"Response: {result}\n")
            
            elif command == "workflow":
                from advanced_features import EXAMPLE_WORKFLOWS, WorkflowEngine
                
                if args in EXAMPLE_WORKFLOWS:
                    engine = WorkflowEngine()
                    print(f"\nExecuting workflow: {args}")
                    result = await engine.execute_workflow(EXAMPLE_WORKFLOWS[args])
                    print(f"Result: {result}\n")
                else:
                    print(f"Available workflows: {list(EXAMPLE_WORKFLOWS.keys())}")
            
            elif command == "plugin":
                if args == "weather":
                    location = input("Enter location: ").strip() or "New York"
                    result = await plugin_mgr.execute_plugin('weather', {'location': location})
                    print(f"\nWeather in {result['location']}:")
                    print(f"  Temperature: {result['temperature']}°C")
                    print(f"  Condition: {result['condition']}")
                    print(f"  Humidity: {result['humidity']}%\n")
                else:
                    print("Available plugins: weather")
            
            elif command == "memory":
                if not args:
                    print("Usage: memory <search query>")
                    continue
                print(f"\nSearching memories for: {args}")
                results = await memory.search_memory(args, limit=5)
                print(f"Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result.get('content', 'N/A')[:100]}...")
                print()
            
            elif command == "health":
                print("\nRunning health check...")
                await health_check()
                print()
            
            elif command == "metrics":
                from advanced_features import AgentMonitor
                monitor = AgentMonitor()
                metrics = monitor.get_metrics()
                print("\nPerformance Metrics:")
                for key, value in metrics.items():
                    print(f"  {key}: {value}")
                print()
            
            elif command == "help":
                print("\nCommands:")
                print("  ask <query>     - Send a query to the agent")
                print("  workflow <name> - Execute a workflow")
                print("  plugin <name>   - Execute a plugin")
                print("  memory <query>  - Search agent memory")
                print("  health          - Check system health")
                print("  metrics         - Show performance metrics")
                print("  help            - Show this help")
                print("  exit            - Exit CLI\n")
            
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Error: {e}")

# ============================================================================
# STRESS TESTING
# ============================================================================

async def stress_test():
    """Stress test the system"""
    print("\n=== STRESS TEST ===\n")
    
    agent = AIAgent()
    
    # Test 1: Rapid fire requests
    print("Test 1: 50 rapid fire requests")
    start = datetime.now()
    tasks = [agent.process_request(f"Query {i}") for i in range(50)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    duration = (datetime.now() - start).total_seconds()
    
    successful = sum(1 for r in results if not isinstance(r, Exception))
    print(f"  Completed in {duration:.2f}s")
    print(f"  Success rate: {successful}/50 ({successful/50*100:.1f}%)")
    print(f"  Throughput: {50/duration:.2f} req/s\n")
    
    # Test 2: Complex workflows
    print("Test 2: 10 complex workflows")
    engine = WorkflowEngine()
    from advanced_features import EXAMPLE_WORKFLOWS
    
    start = datetime.now()
    tasks = [
        engine.execute_workflow(EXAMPLE_WORKFLOWS['daily_research_report'])
        for _ in range(10)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    duration = (datetime.now() - start).total_seconds()
    
    successful = sum(1 for r in results if not isinstance(r, Exception))
    print(f"  Completed in {duration:.2f}s")
    print(f"  Success rate: {successful}/10\n")
    
    # Test 3: Memory stress test
    print("Test 3: 100 memory operations")
    memory = AgentMemory()
    
    start = datetime.now()
    tasks = [
        memory.store_memory(f"Test content {i}", {'index': i})
        for i in range(100)
    ]
    await asyncio.gather(*tasks, return_exceptions=True)
    duration = (datetime.now() - start).total_seconds()
    
    print(f"  Completed in {duration:.2f}s")
    print(f"  Throughput: {100/duration:.2f} ops/s\n")

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

async def main():
    """Main test runner with menu"""
    
    print("\n" + "="*60)
    print("AI AGENT TESTING SUITE")
    print("="*60)
    print("\nSelect test mode:")
    print("1. Run unit tests")
    print("2. Run integration tests")
    print("3. Run all tests")
    print("4. Health check")
    print("5. Load test (100 requests)")
    print("6. Stress test")
    print("7. Benchmark")
    print("8. Demo all features")
    print("9. Manual test examples")
    print("10. Interactive CLI")
    print("0. Exit")
    print("="*60)
    
    choice = input("\nEnter choice (1-10): ").strip()
    
    if choice == "1":
        await run_all_tests()
    
    elif choice == "2":
        print("\nRunning integration tests...")
        await test_full_agent_request()
        await test_multi_agent_collaboration()
    
    elif choice == "3":
        await run_all_tests()
    
    elif choice == "4":
        await health_check()
    
    elif choice == "5":
        await load_test(100)
    
    elif choice == "6":
        await stress_test()
    
    elif choice == "7":
        await benchmark_agents()
    
    elif choice == "8":
        await demo_complete_system()
    
    elif choice == "9":
        await manual_test_examples()
    
    elif choice == "10":
        await interactive_test_cli()
    
    elif choice == "0":
        print("Exiting...")
        return
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    asyncio.run(main())


# ============================================================================
# PYTEST CONFIGURATION
# pytest.ini
# ============================================================================
"""
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    asyncio: mark test as async
    slow: mark test as slow running
    integration: mark test as integration test
addopts = 
    -v
    --tb=short
    --strict-markers
"""

# ============================================================================
# CONTINUOUS INTEGRATION CONFIG
# .github/workflows/test.yml
# ============================================================================
"""
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-asyncio pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
"""
# UNIT TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initializes correctly"""
    agent = AIAgent()
    assert agent is not None
    assert len(agent.capabilities) > 0
    print("✓ Agent initialization test passed")

@pytest.mark.asyncio
async def test_web_search():
    """Test web search functionality"""
    search_agent = WebSearchAgent()
    result = await search_agent.search("Python programming")
    
    assert result['status'] == 'success'
    assert 'results' in result
    assert len(result['results']) > 0
    print("✓ Web search test passed")

@pytest.mark.asyncio
async def test_memory_storage():
    """Test memory storage and retrieval"""
    memory = AgentMemory()
    
    # Store memory
    content = "Python is a great programming language"
    metadata = {"topic": "programming", "timestamp": datetime.now().isoformat()}
    
    store_result = await memory.store_memory(content, metadata)
    assert store_result is not None
    
    # Search memory
    search_results = await memory.search_memory("programming language", limit=5)
    assert len(search_results) > 0
    print("✓ Memory storage test passed")

@pytest.mark.asyncio
async def test_plugin_execution():
    """Test plugin system"""
    plugin_manager = PluginManager()
    plugin_manager.register_plugin(WeatherPlugin())
    
    result = await plugin_manager.execute_plugin('weather', {
        'location': 'London'
    })
    
    assert result['location'] == 'London'
    assert 'temperature' in result
    print("✓ Plugin execution test passed")

@pytest.mark.asyncio
async def test_workflow_execution():
    """Test workflow engine"""
    engine = WorkflowEngine()
    
    simple_workflow = {
        'name': 'test_workflow',
        'steps': [
            {
                'name': 'step1',
                'description': 'Search for AI news'
            },
            {
                'name': 'step2',
                'description': 'Analyze results from {step1}'
            }
        ]
    }
    
    result = await engine.execute_workflow(simple_workflow)
    assert result['status'] == 'completed'
    assert len(result['results']) == 2
    print("✓ Workflow execution test passed")

# ============================================================================
# INTEGRATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_full_agent_request():
    """Test complete agent request processing"""
    agent = AIAgent()
    
    result = await agent.process_request(
        "Search for the latest news about artificial intelligence"
    )
    
    assert result is not None
    assert 'status' in result
    print("✓ Full agent request test passed")

@pytest.mark.asyncio
async def test_multi_agent_collaboration():
    """Test multiple agents working together"""
    system = MultiAgentSystem()
    
    result = await system.collaborate(
        "Research Python web frameworks"
    )
    
    assert 'research' in result
    assert 'analysis' in result
    assert 'report' in result
    print("✓ Multi-agent collaboration test passed")

# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test handling multiple concurrent requests"""
    agent = AIAgent()
    
    tasks = [
        agent.process_request(f"Test query {i}")
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    assert len(results) == 10
    print("✓ Concurrent requests test passed")

@pytest.mark.asyncio
async def test_response_time():
    """Test agent response time is acceptable"""
    agent = AIAgent()
    
    start_time = datetime.now()
    await agent.process_request("Quick test query")
    duration = (datetime.now() - start_time).total_seconds()
    
    assert duration < 30  # Should respond in under 30 seconds
    print(f"✓ Response time test passed ({duration:.2f}s)")

# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_invalid_request():
    """Test handling of invalid requests"""
    agent = AIAgent()
    
    try:
        result = await agent.process_request("")
        # Should handle gracefully
        assert result is not None
        print("✓ Invalid request handling test passed")
    except Exception as e:
        pytest.fail(f"Agent failed to handle invalid request: {e}")

@pytest.mark.asyncio
async def test_api_key_missing():
    """Test behavior when API keys are missing"""
    # Temporarily clear API key
    import os
    original_key = os.getenv('GROQ_API_KEY')
    os.environ['GROQ_API_KEY'] = ''
    
    agent = AIAgent()
    result = await agent.process_request("test")
    
    # Should fallback to basic functionality
    assert result is not None
    
    # Restore key
    if original_key:
        os.environ['GROQ_API_KEY'] = original_key
    
    print("✓ Missing API key handling test passed")

# ============================================================================
# EXAMPLE TEST SCENARIOS
# ============================================================================

@pytest.mark.asyncio
async def test_research_workflow_scenario():
    """Real-world scenario: Research and report generation"""
    engine = WorkflowEngine()
    
    workflow = {
        'name': 'research_scenario',
        'steps': [
            {
                'name': 'research',
                'description': 'Research recent developments in quantum computing'
            },
            {
                'name': 'analyze',
                'description': 'Analyze the research findings from {research}'
            },
            {
                'name': 'report',
                'description': 'Generate a summary report from {analyze}'
            }
        ]
    }
    
    result = await engine.execute_workflow(workflow)
    
    assert result['status'] == 'completed'
    assert len(result['results']) == 3
    print("✓ Research workflow scenario test passed")

@pytest.mark.asyncio
async def test_email_automation_scenario():
    """Real-world scenario: Email automation"""
    agent = AIAgent()
    
    result = await agent.process_request(
        "Draft an email to the team about our weekly progress"
    )
    
    assert result is not None
    print("✓ Email automation scenario test passed")

# ============================================================================
# RUN ALL TESTS
# ============================================================================

async def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*60)
    print("RUNNING AI AGENT TEST SUITE")
    print("="*60 + "\n")
    
    tests = [
        ("Agent Initialization", test_agent_initialization),
        ("Web Search", test_web_search),
        ("Memory Storage", test_memory_storage),
        ("Plugin Execution", test_plugin_execution),
        ("Workflow Execution", test_workflow_execution),
        ("Full Agent Request", test_full_agent_request),
        ("Multi-Agent Collaboration", test_multi_agent_collaboration),
        ("Concurrent Requests", test_concurrent_requests),
        ("Response Time", test_response_time),
        ("Invalid Request Handling", test_invalid_request),
        ("Missing API Key Handling", test_api_key_missing),
        ("Research Workflow Scenario", test_research_workflow_scenario),
        ("Email Automation Scenario", test_email_automation_scenario),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\nRunning: {test_name}")
            await test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_name} FAILED: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return passed, failed

# ============================================================================
# MANUAL TEST EXAMPLES
# ============================================================================

async def manual_test_examples():
    """Interactive examples for manual testing"""
    
    print("\n=== MANUAL TEST EXAMPLES ===\n")
    
    agent = AIAgent()
    
    # Example 1: Simple query
    print("1. Simple Query Test")
    result = await agent.process_request("What can you help me with?")
    print(f"Result: {result}\n")
    
    # Example 2: Research task
    print("2. Research Task Test")
    result = await agent.process_request(
        "Research the top 3 trends in artificial intelligence for 2025"
    )
    print(f"Result: {result}\n")
    
    # Example 3: Code generation
    print("3. Code Generation Test")
    result = await agent.process_request(
        "Write a Python function to calculate fibonacci numbers"
    )
    print(f"Result: {result}\n")
    
    # Example 4: Data analysis
    print("4. Data Analysis Test")
    result = await agent.process_request(
        "Analyze sales data and identify trends"
    )
    print(f"Result: {result}\n")
    
    # Example 5: Multi-step workflow
    print("5. Multi-Step Workflow Test")
    engine = WorkflowEngine()
    workflow = {
        'name': 'manual_test_workflow',
        'steps': [
            {'name': 'search', 'description': 'Search for Python tutorials'},
            {'name': 'summarize', 'description': 'Summarize findings from {search}'},
        ]
    }
    result = await engine.execute_workflow(workflow)
    print(f"Result: {result}\n")

# ============================================================================
# LOAD TESTING
# ============================================================================

async def load_test(num_requests: int = 100):
    """Load test the agent system"""
    print(f"\n=== LOAD TEST: {num_requests} requests ===\n")
    
    agent = AIAgent()
    start_time = datetime.now()
    
    tasks = [
        agent.process_request(f"Test query {i}")
        for i in range(num_requests)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    duration = (datetime.now() - start_time).total_seconds()
    successful = sum(1 for r in results if not isinstance(r, Exception))
    failed = num_requests - successful
    
    print(f"Total Requests: {num_requests}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Duration: {duration:.2f}s")
    print(f"Requests/Second: {num_requests/duration:.2f}")
    print(f"Avg Response Time: {duration/num_requests:.2f}s")

# ============================================================================
# BENCHMARK TESTS
# ============================================================================

async def benchmark_agents():
    """Benchmark different agent operations"""
    print("\n=== AGENT BENCHMARKS ===\n")
    
    benchmarks = {
        'Web Search': lambda: WebSearchAgent().search("test query"),
        'Memory Store': lambda: AgentMemory().store_memory("test", {}),
        'Plugin Execute': lambda: WeatherPlugin().execute({'location': 'NYC'}),
    }
    
    for name, operation in benchmarks.items():
        start = datetime.now()
        
        try:
            await operation()
            duration = (datetime.now() - start).total_seconds()
            print(f"{name}: {duration:.3f}s")
        except Exception as e:
            print(f"{name}: FAILED ({e})")

# ============================================================================
