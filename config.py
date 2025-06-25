import os
from dotenv import load_dotenv

## Config Class

class Config:
    
    def __init__(self):
        load_dotenv()
        self.open_api_key = os.getenv('OPENAI_API_KEY')
        self.grok_api_key = os.getenv('GROK_API_KEY')
        self.openweather_api_key = os.getenv('OPENWEATHER_API_KEY')
        self.exchange_rate_api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        self.serpapi_key = os.getenv('SERPAPI_KEY')
        self.serper_api_key = os.getenv('SERPER_API_KEY')