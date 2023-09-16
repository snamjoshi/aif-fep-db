from pydantic import BaseModel
from typing import List


class TaggedPapers(BaseModel):
    id: str
    tag: str


class MetaDataModel(BaseModel):
    """ Pydantic base model for metadata """
    category: str   # Tag category
    tag_list: List[str] 
    tagged_papers: TaggedPapers
