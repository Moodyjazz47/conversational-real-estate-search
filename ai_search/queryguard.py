import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class QueryGuard:

    def __init__(self, model_3b: str = 'qwen2.5:3b', model_1b:str = os.getenv('OLLAMA_MODEL_CUSTOM') ,
                 local_ollama_url: str = 'http://localhost:11434', ):
        self.model_3b = model_3b
        self.model_1b = model_1b
        self.local_model_url = f"{local_ollama_url}/api/generate"




    def classify(self, query: str):

        prompt = f"""You are a classifier for a real estate search engine.
Classify the user query into ONE of the following categories and return ONLY JSON:

1. REAL_ESTATE
   A valid real estate search query. (e.g."rent a 4bhk flat","villas for sale","show me land near hebbal")

2. NOT_REAL_ESTATE
   Completely unrelated to real estate. (e.g."how to make pasta","play some music")

{{
"classification": REAL_ESTATE | NOT_REAL_ESTATE
}}

User query: {query}
"""

        payload={
            "model":self.model_3b,
            "prompt":prompt,
            "stream":False,
            "format":"json", #enforces json
            "options": {
                    "temperature":0,
                    "stop": ["<|im_end|>"]
        }
        }
        try:
            response = requests.post(self.url_3b, json=payload)
            response.raise_for_status()  #automatically trigger error if phone call to server failed
            data = response.json()
            return json.loads(data["response"])

        except Exception as e:
            return {"error": str(e)}





    def invalid_explanation(self,query:str):
        # We tell the 1B model exactly who it is and what the mistake was
        prompt = f"""
        You are a friendly Real Estate AI Assistant. 
        The user asked: "{query}"
        which is completely unrelated to real estate.

        Be funny/friendly about their off-topic query, then pivot the subject back to property search.
        
        Rules:
        -Keep it under 3 sentences.
        -Do not assume what the user wants if no details are provided
        """

        payload={
            "model":self.model_1b,
            "prompt":prompt,
            "stream":False,
            "options": {
                    "temperature":0.7,
        }
        }

        try:
            response = requests.post(self.local_model_url, json=payload)
            response.raise_for_status()
            data = response.json()

            # FIX: Just return the string. Do NOT use json.loads() here!
            return data["response"]

        except Exception as e:
            return f"Sorry, I'm having trouble connecting. (Error: {str(e)})"