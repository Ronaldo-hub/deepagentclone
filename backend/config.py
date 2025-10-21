import os

class Config:
    SUPABASE_URL = os.getenv('SUPABASE_URL', '')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

