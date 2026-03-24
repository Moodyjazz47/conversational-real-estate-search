# from prompt import EntityExtractor
# from queryguard import QueryGuard
#
# guard = QueryGuard()
#
# # extractor = EntityExtractor()
#
# user_query = "rent a 2 bhk apartment on the moon"
#
# # result = extractor.extract(user_query=user_query)
# guard_result = guard.classify(query=user_query)
#
# print(guard_result)
#
# classification = guard_result["classification"]
#
#
# print(classification)


# from pymilvus import MilvusClient
#
# # Connect to Milvus Lite, storing data in "milvus_demo.db"
# client = MilvusClient("./milvus_demo.db")
#
#
# # Define collection name and dimension (e.g., 384 for a common embedding model)
# client.create_collection(
#     collection_name="demo_collection",
#     dimension=384
# )
#
#
# import numpy as np
#
# # Text strings to search from.
# docs = [
#     "Artificial intelligence was founded as an academic discipline in 1956.",
#     "Alan Turing was the first person to conduct substantial research in AI.",
#     "Born in Maida Vale, London, Turing was raised in southern England.",
# ]
#
# # Generate fake vectors (for illustration)
# # In practice, use a model (e.g., model.encode(docs))
# embeddings = [np.random.rand(384).tolist() for _ in docs]
# ids = list(range(len(docs)))
#
# data = [
#     {"id": i, "text": doc, "vector": emb} for i, (doc, emb) in enumerate(zip(docs, embeddings))
# ]
#
# client.insert(
#     collection_name="demo_collection",
#     data=data
# )
#
#
# # Example query text
# query_text = "Who researched AI?"
#
# # Generate embedding for the query (again, using a real model in practice)
# query_embedding = np.random.rand(384).tolist()
#
# # Perform a vector search for similar texts
# results = client.search(
#     collection_name="demo_collection",
#     data=[query_embedding],
#     limit=2, # Return top 2 results
#     output_fields=["text"], # Return the original text field
# )
#
# # Print the results
# print("Search results:")
# for hit in results[0]:
#     print(f"* Matched text: {hit['entity']['text']}, distance: {hit['distance']}")

import json







def compute_metadata(entities, results, summary):
    formatted_results = []

    for item in results:
        clean_result = {  # one result
            "id": item.get("id"),
            "prop_type_id": item.get("prop_type_id"),
            "prop_name": item.get("prop_name"),
            "location": item.get("property_attr").get("location", {})
        }

        formatted_results.append(clean_result)

    metadata = {
        "entities": entities,
        "results": formatted_results,
        "summary": summary,
    }

    return json.dumps(metadata, default=str)

db_result = [{"id": 115, "prop_type_id": 1012}]

metadata = compute_metadata(entities=['yo'],summary=['gurt'],results=db_result)
print(metadata)


