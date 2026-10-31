augmentation step:
after retrieving we are taking the top k relevant chunks
so here we should make the augmentation step means preparing the prompt to load it into the model
preparing the prompt : make it fits within the max_token content 
Token : could be a word (tokenizer splits the chunks into tokens)
prompt will be made of : chunks, instruction, question

Augmentation must do four things:
1. Receive the question and the retrieved Chunk objects.
2. Select chunks that fit within the token budget.
3. Build a prompt using instructions, selected source text, and the question.
4. Return both the prepared prompt and the selected chunks, so your final answer can preserve the correct source metadata.

Important: 
the token budget is for the complete prompt, not just the chunks. 
We'll also reserve space for Qwen's generated answer.

Augmentation chooses the chunks that fit and combines them with your question into one prompt.



Tokenizer:
Tokenizer in our RAG project:

tokenizer as a translator between human-readable text and the numerical input/output the model uses.

A tokenizer=> is a tool that converts text into tokens that a language model can process and converts
token IDs back into readable text.(encoding , decoding step)

1. The two main methods
Method	Purpose	Example
tokenizer.encode(text)	Text → token IDs	"Hello" → [...integers...]
tokenizer.decode(token_ids)	Token IDs → text	[...integers...] → "Hello"

The token IDs shown above are illustrative; actual IDs depend on the tokenizer.
2. Why do we use a tokenizer?
- During augmentation: encode() helps count tokens so we can select chunks that fit within our token budget.
- During generation: Qwen processes token IDs and generates new token IDs.
- After generation: decode() converts the generated IDs into a readable answer.


- encode() converts the prompt into token IDs.
- len() counts those IDs.
- add_special_tokens=True allows applicable special tokens to be added.

4. Our RAG pipeline
1. Retrieval — BM25 finds relevant chunks.

2. Augmentation — Select chunks and build the prompt.

3. Encoding — Count prompt tokens and prepare model input.

4. Generation — Qwen generates token IDs.

5. Decoding — Convert generated IDs into a readable answer.


The key idea: encode() helps us prepare and measure the model's input, while decode() helps us read the model's output.


photo that shows the relation between tokenizer and LLM:
