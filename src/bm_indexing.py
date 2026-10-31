from .collect_chunks import collect_chunks
import re
import pickle
from rank_bm25 import BM25Okapi
from pathlib import Path


def tokenize(text):
    text = text.lower()
    words = re.findall(r"\b\w+\b", text)

    tokens = []

    for word in words:
        tokens.append(word)

        if "_" in word:
            tokens.extend(part for part in word.split("_") if part)

    return tokens


def index(max_chunk_size = 2000):
  max_chunk_size = int(max_chunk_size)
  chunks = collect_chunks(max_chunk_size)
  
  # each item represent the text of each chunk
  list_texts = [chunk.text for chunk in chunks]
  
  #here then we are taking each item and splitting it into words 
  #ex: ["hello world, lara"] => ["hello", "world", "lara"]
  tokenized_corpus = [
    tokenize(text)
    for text in list_texts
  ]
  #BM25 receives the entire tokenized corpus
  #bm25 = BM25Okapi(tokenized_corpus)

  #Now BM25 builds its internal data based on all the chunks together.
  #It uses information such as:

  #which words occur in each chunk
  #how many times words occur
  #how common/rare words are across the whole corpus
  #how long each chunk is

  #So BM25 is not just storing one value for each chunk.
  #It stores the information needed to calculate a relevance score when a query arrives.
  bm25 = BM25Okapi(tokenized_corpus)
  
  index = {
    "bm25": bm25,
    "chunks": chunks
  }

  processed_dir = Path("data/processed")
  processed_dir.mkdir(parents=True, exist_ok=True)

  index_path = processed_dir / "bm25_index.pkl"

  with open(index_path, "wb") as file:
      pickle.dump(index, file)
  print("Ingestion complete! Indices saved under data/processed/")

  