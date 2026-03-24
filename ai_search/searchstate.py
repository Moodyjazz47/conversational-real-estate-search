from pydantic import BaseModel, Field
from typing import List, Optional


# class PropertyAttributes(BaseModel):
#     """
#     State schema for property attributes to be used in ExtractedEntities()
#     """
#     bedrooms: Optional[str] = None
#     price: Optional[str] = None
#     area_size: Optional[str] = None
#


class ExtractedEntities(BaseModel):
    """
    State schema for extracted entities to be used in the 'FINAL' SearchState()
    """
    customer_intent: List[str] = Field(default_factory=list) #Same as writing 'customer_intent: List[str] = []'
    listing: List[str] = Field(default_factory=list) #default_factory uses a callable
    property_type: List[str] = Field(default_factory=list) #such as a class or a function that will be executed
    property_attributes: List[str] = Field(default_factory=list) #to generate a default value for a field
    location: List[str] = Field(default_factory=list)