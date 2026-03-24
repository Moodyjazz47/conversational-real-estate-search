import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("rules.json") as f:
    rules = json.load(f)

texts = [r["rule"] for r in rules]

embeddings = model.encode(texts)

for i, rule in enumerate(rules):
    rule["embedding"] = embeddings[i].tolist()

with open("rules_with_vectors.json", "w") as f:
    json.dump(rules, f, indent=2)

print("Embeddings created")