from pydantic import BaseModel


#The relationship between the three classes
#   MinimalSource:
#     Describes one source location: file path, start index, and end index.


#MinimalSearchResults
#   Contains one question and its list of retrieved MinimalSource objects.


#StudentSearchResults
#   Contains all the MinimalSearchResults objects for a dataset, plus k.

class MinimalSource(BaseModel):
  file_path: str
  first_character_index: int
  last_character_index: int
