# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama import OllamaLLM
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.runnables import RunnableLambda, RunnableSerializable
# from pydantic import BaseModel, ValidationError
# from searchstate import ExtractedEntities

import os, requests, json
from dotenv import load_dotenv

load_dotenv()


class EntityExtractor:

    def __init__(self, model_3b: str = 'qwen2.5:3b', model_1b:str = os.getenv('LLAMA1B') ,
                 local_ollama_url: str = os.getenv('LOCAL_MODEL_API_URL') ):
        self.model_3b = model_3b
        self.model_1b = model_1b
        self.local_ollama_url = f"{local_ollama_url}/api/generate"


        # self.llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

    def extract(self, user_query:str):

        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You extract property search filters from real estate queries.
Return valid JSON only. Do not explain.

Do not generate property listings.
Do not generate prices or property data.
Only extract entities mentioned in the query.

Output schema:
{{
 "listing_type": [],
 "property_type": [],
 "property_attributes": [],
 "location": []
}}

Rules:
- Extract values only if the user explicitly mentions them.
- If a field is not mentioned, return an empty list.
<|eot_id|>

<|start_header_id|>user<|end_header_id|>I want to rent a single bedroom house in hebbal<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
{{"listing_type":["rent"],"property_type":["house"],"property_attributes":["single bedroom"],"location":["hebbal"]}}<|eot_id|>

<|start_header_id|>user<|end_header_id|>show me some 2bhk apartments<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
{{"listing_type":[],"property_type":["apartments"],"property_attributes":["2bhk"],"location":[]}}<|eot_id|>

<|start_header_id|>user<|end_header_id|>interested in purchasing a villa near mg road<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
{{"listing_type":['sale'],"property_type":["villa"],"property_attributes":[],"location":["mg road"]}}<|eot_id|>

<|start_header_id|>user<|end_header_id|>{user_query}<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

        payload = {
        "model": self.model_1b,
        "prompt": prompt,
        "stream": False,
        "format": "json",  # enforces json
        "options": {
            "temperature": 0,
            "stop": ["<|eot_id|>", "<|end_of_text|>"]
        }
    }

        try:
            response = requests.post(self.local_ollama_url, json=payload)
            response.raise_for_status()  # automatically trigger error if phone call to server failed
            data = response.json()
            return json.loads(data["response"])

        except Exception as e:
            return {"error": str(e)}