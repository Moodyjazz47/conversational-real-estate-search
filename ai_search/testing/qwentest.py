
import os, requests, json
from dotenv import load_dotenv

load_dotenv()


class EntityExtractor:

    def __init__(self, model_3b: str = 'qwen2.5:3b', qwen_url_3b: str = os.getenv('LOCAL_MODEL_API_URL')):

        self.model_3b = model_3b
        self.model_url = f"{qwen_url_3b}/api/generate"


        # self.llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash')

    def extract(self, user_query:str):

        prompt = f"""<|im_start|>system
You extract property search filters from real estate queries:listing type, property type, property attributes, location
Return valid JSON only. Do not explain.

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
- If a field is not mentioned, return an empty list.<|im_end|>

<|im_start|>user
I want to rent a single bedroom house in hebbal<|im_end|>
<|im_start|>assistant
{{"listing_type": ["rent"], "property_type": ["house"], "property_attributes": ["single bedroom"], "location": ["hebbal"]}}<|im_end|>

<|im_start|>user
show me some 2bhk apartments<|im_end|>
<|im_start|>assistant
{{"listing_type": [], "property_type": ["apartments"], "property_attributes": ["2bhk"], "location": []}}<|im_end|>

<|im_start|>user
interested in purchasing a villa near mg road<|im_end|>
<|im_start|>assistant
{{"listing_type": ["sale"], "property_type": ["villa"], "property_attributes": [], "location": ["mg road"]}}<|im_end|>

<|im_start|>user
i want to look at some houses<|im_end|>
<|im_start|>assistant
{{"listing_type": [], "property_type": ["houses"], "property_attributes": [], "location": []}}<|im_end|>

<|im_start|>user
{user_query}<|im_end|>
<|im_start|>assistant
"""


        payload = {
        "model": self.model_3b,
        "prompt": prompt,
        "stream": False,
        "format": "json",  # enforces json
        "options": {
            "temperature": 0,
            "stop": ["<|im_end|>"]
        }
    }

        try:
            response = requests.post(self.model_url, json=payload)
            response.raise_for_status()  # automatically trigger error if phone call to server failed
            data = response.json()
            return json.loads(data["response"])

        except Exception as e:
            return {"error": str(e)}