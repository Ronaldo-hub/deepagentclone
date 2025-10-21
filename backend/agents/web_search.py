class WebSearchAgent:
    async def search(self, query: str):
        return {'status': 'success', 'query': query, 'results': []}
