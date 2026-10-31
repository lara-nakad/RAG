from typing import List
from .chunk import Chunk
from .MinimalSource import MinimalSource

def convert_chunks_minimal(chunks: List[Chunk])->List[MinimalSource]:
  res:List[MinimalSource] = []
  
  for chunk in chunks:
      res.append(
        MinimalSource(
          file_path = chunk.file_path,
          first_character_index = chunk.first_character_index,
          last_character_index = chunk.last_character_index
        )
      )
  
  return res

