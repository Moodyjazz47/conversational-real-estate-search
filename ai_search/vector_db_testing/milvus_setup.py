from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

connections.connect("default", host="localhost", port="19530")

fields = [
    FieldSchema(name="rule_id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="rule_text", dtype=DataType.VARCHAR, max_length=500),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384)
]   #why 384: all-MiniLM-L6-v2(our embedding model) → 384 embedding size

schema = CollectionSchema(fields)

collection = Collection("real_estate_rules", schema)

print("Collection created")