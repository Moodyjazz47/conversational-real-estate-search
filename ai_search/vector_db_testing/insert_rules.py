import json
from pymilvus import Collection

collection = Collection("real_estate_rules")

with open("rules_with_vectors.json") as f:
    rules = json.load(f)

ids = []
texts = []
vectors = []

for r in rules:
    ids.append(r["id"])
    texts.append(r["rule"])
    vectors.append(r["embedding"])

collection.insert([ids, texts, vectors])

collection.flush()

print("Rules inserted")