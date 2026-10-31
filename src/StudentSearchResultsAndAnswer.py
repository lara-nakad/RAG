from .MinimalAnswer import MinimalAnswer
from typing import List
from pydantic import BaseModel

class StudentSearchResultsAndAnswer(BaseModel):
	search_results : List[MinimalAnswer]
	k : int
