from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnableSerializable
from pydantic import BaseModel, ValidationError
from searchstate import ExtractedEntities

import os, requests, json, re
from dotenv import load_dotenv

load_dotenv()


class EntityExtractor:

    def __init__(
        self,
        model_3b: str = "qwen2.5:3b",
        model_1b: str = os.getenv("OLLAMA_MODEL_CUSTOM"),
        ollama_url_3b: str = os.getenv("LOCAL_MODEL_API_URL"),
        ollama_url_1b: str = os.getenv("OLLAMA_API_URL"),
    ):
        self.model_3b = model_3b
        self.model_1b = model_1b
        self.url_3b = f"{ollama_url_3b}/api/generate"
        self.url_1b = f"{ollama_url_1b}/api/generate"

    def _safe_json_parse(self, text: str):
        """Extract JSON safely even if the model adds extra text."""
        try:
            return json.loads(text)
        except Exception:
            match = re.search(r"\{.*?\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
            raise

    def extract(self, user_query: str):

        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You extract structured search filters from real estate queries.

Return valid JSON only. Do not explain.

Normalize similar words:
buy, purchase, acquire → sale
lease, renting → rent
office facility, office space → office
3 bedroom → 3bhk

Do not generate property listings.
Do not generate prices or property data.

Output schema:
{{
 "listing_type": [],
 "property_type": [],
 "property_attributes": [],
 "location": []
}}

Rules:
- Only extract entities explicitly mentioned.
- If a field is missing, return an empty list.

<|eot_id|>

<|start_header_id|>user<|end_header_id|>
I want to rent a single bedroom house in hebbal
<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
{{"listing_type":["rent"],"property_type":["house"],"property_attributes":["single bedroom"],"location":["hebbal"]}}
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
show me some 2bhk apartments
<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
{{"listing_type":[],"property_type":["apartments"],"property_attributes":["2bhk"],"location":[]}}
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
interested in purchasing a villa near mg road
<|eot_id|>

<|start_header_id|>assistant<|end_header_id|>
{{"listing_type":["sale"],"property_type":["villa"],"property_attributes":[],"location":["mg road"]}}
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
{user_query}
<|eot_id|>
Respond with one JSON object only.
<|start_header_id|>assistant<|end_header_id|>
"""

        payload = {
            "model": self.model_1b,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0,
                "num_predict": 120,
                "stop": ["<|eot_id|>", "<|end_of_text|>"]
            }
        }

        try:
            response = requests.post(self.url_1b, json=payload)
            response.raise_for_status()
            data = response.json()

            parsed = self._safe_json_parse(data["response"])

            # Ensure schema stability
            for key in ["listing_type", "property_type", "property_attributes", "location"]:
                if key not in parsed:
                    parsed[key] = []

            return parsed

        except Exception as e:
            return {"error": str(e)}