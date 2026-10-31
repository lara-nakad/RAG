from pydantic import BaseModel

class Chunk(BaseModel):
    file_path:str
    text:str
    first_character_index:int
    last_character_index:int

