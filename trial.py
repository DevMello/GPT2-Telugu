from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import torch


model = GPT2LMHeadModel.from_pretrained("telugu-gpt2-small")
tokenizer = GPT2TokenizerFast.from_pretrained("telugu-gpt2-small")


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()


prompt = "తెలుగు భాషలో పురాణాలు" 

inputs = tokenizer(prompt, return_tensors="pt").to(device)

output = model.generate(
    **inputs,
    max_length=512,
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.9,
    pad_token_id=tokenizer.pad_token_id,
    eos_token_id=tokenizer.eos_token_id
)

generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(generated_text)
print("Output written to output.txt")
