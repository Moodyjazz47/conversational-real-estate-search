import json

#prompt classes
from queryguard import QueryGuard
from testing.qwentest import EntityExtractor



#postprocessing classes
from entity_postprocessing.entity_normalization import EntityNormalizer
from entity_postprocessing.canonical_mapping import CanonicalMapper
from entity_postprocessing.query_builder import QueryBuilder
from entity_postprocessing.query_executor import QueryExecutor, DBConfig
from entity_postprocessing.result_summarizer import ResultSummarizer

from dotenv import load_dotenv
import os

from typing import Dict

guard = QueryGuard()
extractor = EntityExtractor()
result_summarizer = ResultSummarizer()

load_dotenv()
db_config = DBConfig(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    db_name=os.getenv("DB_NAME"),
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    min_conn=int(os.getenv("DB_MIN_CONN", 1)),
    max_conn=int(os.getenv("DB_MAX_CONN", 5))
)
query_executor = QueryExecutor(db_config)



def extracting(user_query:str)->Dict:
    entities = extractor.extract(user_query)
    return entities


def executing(entities:Dict)->str:
    """
    passes final entities list,
    apply canonical mapping,
    calls query builder,
    executes query,
    stores results
    """
    normalized = EntityNormalizer.normalize_entities(entities)
    canonical = CanonicalMapper.map_entities(normalized)
    sql_query, params =QueryBuilder.build_full_query(canonical)
    results = query_executor.execute(sql_query,params)
    print(sql_query,params)
    return results




def compute_metadata(entities,results,summary):

    formatted_results = []

    for item in results:

        clean_result = {       #one result
            "id" : item.get("id"),
            "prop_type_id" : item.get("prop_type_id"),
            "prop_name" : item.get("prop_name"),
            "location": item.get("property_attr").get("location",{})
        }

        formatted_results.append(clean_result)

    metadata = {
        "entities":entities,
        "results":formatted_results,
        "summary":summary,
    }

    return json.dumps(metadata, default=str)



def main(user_query:str)->dict:
    guard_result = guard.classify(user_query)
    classification = guard_result["classification"]
    print(classification)
    if classification != "REAL_ESTATE":
        response = guard.invalid_explanation(query=user_query)
        return response

    extracted_entities = extracting(user_query)
    print(f'\nextracted entities:{extracted_entities}\n')
    result = executing(extracted_entities)
    print(result)
    if not result:
        return "Sorry, looks like we could'nt find any properties as per your requirements. Would you like to refine your search?"

    else:
        result_summary = result_summarizer.summarize(result)
        metadata = compute_metadata(entities=extracted_entities,results=result, summary=result_summary)
        print(metadata)
        return metadata



main(user_query='Im looking to buy or rent a flat')
#sample queries: 
#"want to rent an office space near hebbal",  "something with 3 bedrooms",  "show me properties for sale near whitefield",  "flats for rent",  "I want a house", "a 3bhk house for rent in yelahanka" etc.

    # sample_dict = {"customer_intent": ["RENT"], 'listing':["rent"], "property_type": ["duplex"], "property_attributes":["4 bedroom"], "location":["mg road"]  }
    # extracted_entities = ExtractedEntities(**sample_dict)
