from rule_retriever import retrieve_rules
import os, requests, json
from dotenv import load_dotenv

load_dotenv()


class RAGValidator:

    def __init__(self, model_3b: str = 'qwen2.5:3b', model_1b:str = os.getenv('OLLAMA_MODEL_CUSTOM') ,ollama_url: str = 'http://localhost:11434'):
        self.model_3b = model_3b
        self.model_1b = model_1b
        self.url = f"{ollama_url}/api/generate"


    def validate(self, query):

        rules = retrieve_rules(query)

        context = "\n".join(rules)

        prompt = f"""
User query: {query}

Relevant real estate rules:
{context}

Based on these rules determine if the query is VALID_REAL_ESTATE or INVALID_REAL_ESTATE.

Respond in JSON:

{{
 "classification": "VALID_REAL_ESTATE | INVALID_REAL_ESTATE",
 "reason": "short explanation"
}}
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
            response = requests.post(self.url, json=payload)
            response.raise_for_status()  #automatically trigger error if phone call to server failed
            data = response.json()
            return json.loads(data["response"])

        except Exception as e:
            return {"error": str(e)}