from pathlib import Path
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json


def load_index():
  #it gives us the file path
  index_path = Path("data/processed/tfidf_index.pkl")
  
  with open(index_path, "rb") as fd:
    index = pickle.load(fd)
  
  return index


def search_dataset(dataset_path, k, save_directory):
  index = load_index()
  
  with open(dataset_path, "r") as fd:
    #here to load the json data
    dataset_content = json.load(fd)
    
  results = []
  rag_questions = dataset_content["rag_questions"]
  for question in rag_questions:
    question_id = question["question_id"]
    question_statement = question["question"]
    
    top_chunks = retrieve(question_statement, k, index)
    recieved_chunks_info = []
    for chunk in top_chunks:
      recieved_chunks_info.append({
        "file_path":chunk.file_path,
        "first_character_index":chunk.first_character_index,
        "last_character_index":chunk.last_character_index,
      })

    results.append({
    "question_id": question_id,
    "question": question_statement,
    "retrieved_sources": recieved_chunks_info
    })
  
  output = {
    "search_results": results,
    "k": k
  }
  
  output_directory = Path(save_directory)
  output_directory.mkdir(parents=True, exist_ok=True)

  output_path = output_directory / "search_results.json"

  with open(output_path, "w") as fd:
      json.dump(output, fd, indent=2)

  print(f"Saved search results to: {output_path}")


def retrieve(query, k, index):
  vectorizer = index["vectorizer"]
  vectors = index["vectors"]
  chunks = index["chunks"]
  #Existing vectorizer (we are using the pre trained vectorizer for vocabs and TF_IDF values)
       #│
       #│ already knows
       #│ vocabulary + IDF
       #↓
  #"What is the default CUDA graph size?"
       #↓
  #TF-IDF vector using SAME representation
       #↓
  #query vector
  #transform takes a collection of documents so that's why we are inserting it as a list not as a raw string
  query_vector = vectorizer.transform([query])
  #here scores should be equal to the number of chunks since each value represents the cosine similarity between the query and each chunk
  scores = cosine_similarity(query_vector, vectors)
  scores = scores[0]
  #here it gives us the indices from small to large yaane highest value bekun l index taaeta bl ekher
  indices = np.argsort(scores)
  #here we took the top indices (from small to large)
  indices = indices[-k:]
  #here we arrange them from large to small
  indices = indices[::-1]
  
  res_top_chunks = []
  for i in indices:
    res_top_chunks.append(chunks[i])

    
  return res_top_chunks

def main():
  index = load_index()
  #print(index.keys())
  print(retrieve("What hardware platforms does vLLM support?", 5, index))
  #search_dataset("datasets_public/public/UnansweredQuestions/dataset_docs_public.json", 5,  "data/output/search_results/UnansweredQuestions")
  
  
if __name__ == "__main__":
  main()