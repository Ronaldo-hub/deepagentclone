import asyncio
from backend.main import AIAgent

class Worker:
    def __init__(self):
        self.agent = AIAgent()

    async def run_once(self, message: str):
        return await self.agent.process_request(message)
