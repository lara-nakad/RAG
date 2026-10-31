import pickle
from pathlib import Path
import json
import numpy
from .bm_indexing import tokenize
from .chunks_minimal_conversion import convert_chunks_minimal
from .MinimalSearchResults import MinimalSearchResults 
from .StudentSearchResult import StudentSearchResult 

def load_bm25_index():
    index_path = Path("data/processed/bm25_index.pkl")

    with open(index_path, "rb") as file:
        index = pickle.load(file)

    return index


def search_dataset(dataset_path, k, save_directory):
    index = load_bm25_index()

    with open(dataset_path, "r") as fd:
        # Load the dataset JSON
        dataset_content = json.load(fd)

    results = []
    rag_questions = dataset_content["rag_questions"]

    received_chunks_info = []
    
    for question in rag_questions:
        question_id = question["question_id"]
        question_statement = question["question"]

        top_chunks = retreving(question_statement, k, index)
        minimalSources = convert_chunks_minimal(top_chunks)
        
        minimalSearchResult = MinimalSearchResults(
            question_id = question_id,
            question = question_statement,
            retrieved_sources = minimalSources
        )
        received_chunks_info.append(minimalSearchResult)

    student_results = StudentSearchResult(
        search_results = received_chunks_info,
        k = k
    )

    # Create the output directory if it doesn't exist
    output_directory = Path(save_directory)
    output_directory.mkdir(parents=True, exist_ok=True)

    # Keep the same filename as the input dataset
    dataset_filename = Path(dataset_path).name
    output_path = output_directory / dataset_filename

    # Save the Pydantic object as JSON
    with open(output_path, "w", encoding="utf-8") as fd:
        #model_dump_json() -> converts your Pydantic object directly into a JSON string.
        fd.write(student_results.model_dump_json(indent=2))

    print(f"Saved student_search_results to {output_path}")


def retreving(query, k, index):
    bm25 = index["bm25"]
    chunks = index["chunks"]

    query_corpus = tokenize(query)
    scores = bm25.get_scores(query_corpus)

    # Get the indices of the k highest scores
    indices = numpy.argsort(scores)
    indices = indices[-k:]
    #from highest to lowest saru
    indices = indices[::-1]

    res_top_chunks = []

    for i in indices:
        res_top_chunks.append(chunks[i])

    return res_top_chunks
  


def search(query, k=5):
    index = load_bm25_index()
    top_chunks = retreving(query, k, index)

    for rank, chunk in enumerate(top_chunks, start=1):
        print(f"Rank: {rank}")
        print(f"File: {chunk.file_path}")
        print(f"Start: {chunk.first_character_index}")
        print(f"End: {chunk.last_character_index}")
        print("-" * 40)
