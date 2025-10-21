"""Minimal FastAPI app and AIAgent shim for tests and local development."""
try:
    from fastapi import FastAPI
except Exception:
    FastAPI = None

from typing import Dict
from datetime import datetime

app = FastAPI() if FastAPI is not None else None

class AIAgent:
    """Lightweight agent shim used by tests and examples."""
    def __init__(self):
        self.capabilities = {
            'web_search': None,
            'code_generation': None
        }

    async def process_request(self, message: str) -> Dict:
        # Very small deterministic fallback response for tests
        return {
            'status': 'success',
            'message': f'Processed: {message}',
            'timestamp': datetime.utcnow().isoformat()
        }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
