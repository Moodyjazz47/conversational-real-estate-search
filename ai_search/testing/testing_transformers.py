from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json


class QueryClassifier:

    def __init__(self, model_path: str, gguf_filename: str):

        print("Loading validator model...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            gguf_file=gguf_filename
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            gguf_file=gguf_filename,
            device_map="auto"
        )

        print("Validator model loaded.")


    def classify(self, user_query: str):

        messages = [
            {
                "role": "system",
                "content": """
You classify queries for a property search engine.

Categories:
REAL_ESTATE
NOT_REAL_ESTATE

Return JSON:
{"classification":"CATEGORY"}
"""
            },

            {"role": "user", "content": "flats for rent"},
            {"role": "assistant", "content": '{"classification":"REAL_ESTATE"}'},

            {"role": "user", "content": "villas in bangalore"},
            {"role": "assistant", "content": '{"classification":"REAL_ESTATE"}'},

            {"role": "user", "content": "I want pizza"},
            {"role": "assistant", "content": '{"classification":"NOT_REAL_ESTATE"}'},

            {"role": "user", "content": user_query}
        ]

        input_ids = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            input_ids,
            max_new_tokens=50,
            temperature=0.1
        )

        response = self.tokenizer.decode(
            outputs[0][input_ids.shape[-1]:],
            skip_special_tokens=True
        )

        try:
            return json.loads(response)
        except:
            return {"classification": "UNKNOWN", "raw_output": response}