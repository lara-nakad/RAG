from pydantic import BaseModel
from .MinimalSearchResults import MinimalSearchResults
from typing import List

class StudentSearchResult(BaseModel):
  search_results : List[MinimalSearchResults]
  k : int