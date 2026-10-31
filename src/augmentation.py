#Augmentation has three main responsibilities:
#1. Load the tokenizer associated with Qwen.
#   Tokenizer is responsible for taking the text transform it into list of token ids
# 	and then we count the number of tokens
#2. Select retrieved chunks that fit within our token budget.
#3. Combine their actual text with the question and instructions into a prompt

from transformers import AutoTokenizer
from typing import List
from .chunk import Chunk

MODEL_NAME = "Qwen/Qwen3-0.6B"

INSTRUCTIONS = (
	"Answer the question using the provided context from the "
    "vLLM repository. Do not invent facts. "
    "If the context is insufficient, explain that."
)

def build_prompt(question: str, context: str):
    """Combine instructions, context, and question."""
    return (
		f"{INSTRUCTIONS}\n\n"
		f"Context: {context}\n\n"
		f"Question: {question}\n\n"
		"Answer:"
	)
    

def count_tokens(prompt: str, tokenizer):
    token_ids = tokenizer.encode(prompt,
								add_special_tokens = True)
    return len(token_ids)



def load_tokenizer():
  """Load the tokenizer associated with our language model."""
  return  AutoTokenizer.from_pretrained(MODEL_NAME)


def select_chunks(question: str, tokenizer, chunks: List[Chunk], token_budget: int):
    """Select chunks that fit within the prompt token budget."""
    
    selected_chunks = []
    if not question.strip():
        raise ValueError("Question cannot be empty")
    
    if token_budget <= 0:
        raise ValueError("Token budget should be at least greater than 1")
    
    prompt = build_prompt(question, "")
    
    if count_tokens(prompt, tokenizer) > token_budget:
        raise ValueError(
			"Question and instructions exceed token budget"
		)
    
    for chunk in chunks:
        candidate_chunks = selected_chunks + [chunk]
        
        context = "\n\n".join(item.text for item in candidate_chunks)
        #here res is the prompt we build as a text
        res = build_prompt(question, context)
        if count_tokens(res, tokenizer) <= token_budget:
            selected_chunks.append(chunk)
            prompt = res
    
    return prompt, selected_chunks
        