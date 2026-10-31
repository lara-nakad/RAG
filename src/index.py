from pydantic import BaseModel
from .chunk import Chunk

class ListChunks(BaseModel):
  chunks : list[Chunk]