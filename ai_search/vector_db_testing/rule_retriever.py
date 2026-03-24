from sentence_transformers import SentenceTransformer
from pymilvus import Collection, connections

# connect to Milvus FIRST
connections.connect(alias='default',
                    host='localhost', #we'll change this if remote
                    port=19530)


model = SentenceTransformer("all-MiniLM-L6-v2")

collection = Collection("real_estate_rules")

def retrieve_rules(query, top_k=3):

    query_vector = model.encode([query])[0]

    results = collection.search(
        data=[query_vector],
        anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=top_k,
        output_fields=["rule_text"]
    )

    rules = []

    for hit in results[0]:
        rules.append(hit.entity.get("rule_text"))

    return rules