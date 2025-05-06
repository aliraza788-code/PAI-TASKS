from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

### Load pre-trained GPT2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

### Set model to evaluation mode
model.eval()

### Input text prompt
prompt = "Artificial Intelligence is transforming the world by"
input_ids = tokenizer.encode(prompt, return_tensors="pt")

### Generate text
output = model.generate(
    input_ids,
    max_length=100,
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    do_sample=True,
    temperature=0.7,
    top_p=0.9
)

### Decode and print the generated text
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated Text:\n", generated_text)
