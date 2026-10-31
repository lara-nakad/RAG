from pathlib import Path
from .python_chunking import python_chunking
from .markdown_chunking import markdown_chunking
from .text_chunking import text_chunk
from .chunk import Chunk

def collect_chunks(max_chunk_size):
    max_chunk_size = int(max_chunk_size)
    res_chunks : list[Chunk] = []
    #it creates a python object to the repo
    root = Path("data/raw/vllm-0.10.1")
    #root.rglob it takes all the subdirectories and files inside the current working directory (noy only direct children inside this repo)
    for p in root.rglob("*"):
        #here inside p we have the full path of the file
        if not p.is_file():
            continue
        extension = p.suffix.lower()
        if extension == ".py":
            chunks = python_chunking(str(p), max_chunk_size)
        elif extension == ".md":
            chunks = markdown_chunking(str(p), max_chunk_size)
        elif extension == ".txt":
            chunks = text_chunk(str(p), max_chunk_size)
        #this case when its is a file but not markdown/ python/ text file
        else:
            continue
        res_chunks.extend(chunks)
    
    return res_chunks

