#main file is responsible for:
#   Receive the user's question.
#   Retrieve the top chunks using BM25.
#   Select chunks that fit the token budget and build the prompt.
#   Generate the answer with Qwen.
#   Return the answer

from .bm_retrieving import load_bm25_index
from .augmentation import load_tokenizer
from .generation import load_model
from .bm_retrieving import retreving
from .augmentation import select_chunks
from .StudentSearchResultsAndAnswer import StudentSearchResultsAndAnswer
from .generation import generate_answer
from .MinimalAnswer import MinimalAnswer
import json
from pathlib import Path
from .chunks_minimal_conversion import convert_chunks_minimal


# Global resources
index = None
tokenizer = None
model = None


def load_resources():
    global index, tokenizer, model

    index = load_bm25_index()
    tokenizer = load_tokenizer()
    model = load_model()
  
  
def answer(question, k, token_budget):
	if model is None or tokenizer is None or index is None:
		load_resources()
	#first we get the relevant chunks
	chunks = retreving(question, k, index)
	#second method augmentation to prepare the chunks and extract the prompt
	prompt, chunks = select_chunks(question, tokenizer, chunks, token_budget)
	if not chunks:
		return ("No relevant chunks fit within the token budget", [])
	relevant_chunks = convert_chunks_minimal(chunks)
	#after recieving the prompt we should generate the answer
	answer = generate_answer(prompt, model, tokenizer)
	return answer, relevant_chunks


def answer_dataset(student_search_results_path, save_directory, k = 5, token_budget = 2000):
	with open(student_search_results_path, "r") as file:
		dataset_content = json.load(file)
	output_directory = Path(save_directory)
	output_directory.mkdir(parents=True, exist_ok=True)
	output_path = output_directory / Path(student_search_results_path).name
	print("Dataset loaded", flush=True)

	dataset_questions = dataset_content["search_results"] #list of rag questions each one is on dict type
	results = []
	load_resources()
	print("Resources loaded successfully", flush=True)

	for question_data in dataset_questions:
		question_id = question_data["question_id"]
		question_text = question_data["question"]
		print(f"Starting question: {question_id}", flush=True)
		relevant_chunks = question_data["retrieved_sources"]
		prompt, chunks = select_chunks(question_text, tokenizer, relevant_chunks, token_budget)
		if not chunks:
			print("No relevant chunks fit within the token budget")
		answer = generate_answer(prompt, model, tokenizer)

		print(f"Finished question: {question_id}", flush=True)
		res = MinimalAnswer(
			question_id = question_id,
			question = question_text,
			retrieved_sources = chunks,
			answer = answer
		)

		results.append(res)
		final_res = StudentSearchResultsAndAnswer(
    		search_results=results,
    		k=k
		)

		with open(output_path, "w", encoding="utf-8") as file:
			file.write(final_res.model_dump_json(indent=2))
    
	print(f"Saved answers to {output_path}")

