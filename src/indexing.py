from .collect_chunks import collect_chunks
from typing import List
from .chunk import Chunk
from sklearn.feature_extraction.text import TfidfVectorizer
from pathlib import Path
import pickle

def save_index(max_chunk_size = 2000):
  chunks : List[Chunk] = collect_chunks(max_chunk_size)
  
  texts = [chunk.text for chunk in chunks]

  #since TF_IDF takes text and converts it to vector (numerical representation)
  #(conversion(numerical representation) btseer based aa each word kam marra mkarara bkl chunk w adei heyye rare bnsbe la kl l chunks)
  #so here we should calculate TF and IDF 
  #TF => how much this word appears b alb l current chunk (bekun aanda high value (values range from 0 -> 1))
  #IDF => how much this word rarely appears with respect to all chunks (la ykun aanda higher value)
  #here we are preparing the object that will perform the IF_IDF
  #Create the machine that knows how to convert text into TF-IDF numbers."
  vectorizer = TfidfVectorizer()
  
  # here we want to save also the tockenizer laen already staamalneh w aarrafneh aal vocabulary w aal matrix vectors
  # fit_transform first we let the vectorizer know the vocabulary then we make the tf_idf generation for each text related to a chunk
  
  #fit => for letting the vectorizer knows the vocabulary (teach the vocab) / and let the vectorizer knows all the TF_IDF values so when we are indexing th equery we are just assiging the previous defined TF_IDF values 
  # transform => for transforming TF_IDF values
  #so here first we make all the words as columns and set values IF_IDF value based on the appearence inside each chunk and among all documents so all TF_IDF values / vocabs will be already known
  #so for every text of a chunk/ query text we put each row m2abeelu kl l columns (vocabs) and since kl vocab aanda TF_IDF value so mnseer ntalle3 lvector la kl text 
  matrix = vectorizer.fit_transform(texts) 
  index = {
    "vectorizer":vectorizer,
    "vectors" : matrix, 
    "chunks": chunks
  }
  
  #after getting the index we should now save it inside data/processed folder
  #so here we will first create the file and save the chunk inside
  processed_dir = Path("data/processed")
  #to make sure this file exists
  processed_dir.mkdir(parents=True, exist_ok=True)
  #to say inside this is the file where we save the index
  index_path = processed_dir / "tfidf_index.pkl"
  with open(index_path, "wb") as file:
    pickle.dump(index, file)

  
def main():
  save_index()

if __name__ == "__main__":
  main()