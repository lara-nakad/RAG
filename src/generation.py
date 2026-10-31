#first step we should load the model
#we should take the model resulting from the augmentation step and encode it into tokens(using tokenizer) in order to let the model understand it
#since model doesn't understand readable text so we should convert it into token ids (using tokenizer) and then pass these token ids into the model 

#Step 1: Load the model
# What are we trying to do?
# Your augmentation code creates a prompt containing the question, instructions, and retrieved context.
#For example:
#Context:
#LoRA adapters extend a model.
#Question:
#What is LoRA?

#Now we need Qwen, our language model, to generate an answer from that prompt.
#Before it can do that, we must load the model into Python.

#to load the model and tokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer

import torch

MODEL_NAME = "Qwen/Qwen3-0.6B"

def load_model():
	"""Load the Qwen language model."""
	#AutoModelForCasualLM is a Transformers class designed for models that generate text.
	#from_pretrained:(To load the pretrained Qwen model), loads the model's configuration and trained parameters.
	#Model_name : identifies the Qwen model we want to load
	#model.eval():puts the model into evaluation mode.
	#return model: get back the model to use it while applying the generation step
	model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
	model.eval()
	return model


def load_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    return tokenizer


def generate_answer(prompt, model, tokenizer):
    #even we prepared the prompt in augmentation step but we should make it fit the Qwen template since the model is a chatting model (so we use chat template)
    #messages holds the whole prompt sent to the model in the format expected by Qwen's chat template.
    #message = [
        #role here to say that the message is coming from the user
		#{"role": "user"},
		#{"content": prompt}
	#]
    messages = [
        {"role": "user", "content": prompt}
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
        enable_thinking=False,
    )
    
	##now after making the message in the Qwen's format we will encode it
    #inputs = tokenizer.apply_chat_template(
        #message,
        #here we will encode
        #tokenize=True,
        #to say this model is now responsible for generating (we are not training it)
        #add_generation_prompt=True,
        #since model uses Pytorch and Pytorch has tensor as a data structure so we are retreving the token ids and save these tokens using this container
        #return_tensors="pt",
        #we are returning the result as a dictionary 
        #return_dict=True,
        #krml ma nfakker enu model will expect to think laen nehna already aam naate l answer maaou
        #enable_thinking=False,
    #)
    #after this result we are getting dict value with keys and values
    #keys are of 2 (input_ids and attention_mask)
    #Key: "input_ids"
	#Value: A tensor containing the token IDs of your prompt.
	#Example: [101, 205, 309]
	#Key: "attention_mask"
	#Value: A tensor indicating which token positions are valid.
    # value associated by input_ids is of tensors container that holds the token_ids as a list
    # second value => PyTorch tensor indicating which input positions should be attended to
    
    #here we are checking on which device the model is running (GPU OR CPU)
    device = next(model.parameters()).device
    
    #here we are making the tensor run on the same device 
    inputs = inputs.to(device)
    
    #here we are unpacking 
    output = model.generate(**inputs, max_new_tokens = 256, do_sample=False)
    #this one is equivalence to model.generate(input_ids = inputs["input_ids"], attention_mask = inputs{"attention_mask"})
    #here we are unpacking the values so here we are taking the token_ids and sent them to the model and output also will be of token ids
    
    #here we get the length of token_ids (input token ids)
    #inputs["input_ids"] accesses the input token IDs.
    #.shape tells us the dimensions of the tensor.
    #[1] selects the second dimension: the number of tokens in the input sequence.
    
    input_length = inputs["input_ids"].shape[1]
    generated_tokens = output[0][input_length:]
    answer = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
    
    return answer