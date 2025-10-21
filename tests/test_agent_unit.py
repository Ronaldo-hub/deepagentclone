import asyncio
from backend.main import AIAgent


def test_agent_process_request():
    agent = AIAgent()
    result = asyncio.run(agent.process_request('hello'))
    assert isinstance(result, dict)
    assert result['status'] == 'success'
