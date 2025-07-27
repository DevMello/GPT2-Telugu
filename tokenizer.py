from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2TokenizerFast
import os

tokenizer = ByteLevelBPETokenizer()

output_dir = "telugu-tokenizer"
os.makedirs(output_dir, exist_ok=True)

tokenizer.train(
    files=["data/books.txt", "data/news_website_cleaned.txt"],
    vocab_size=50257,
    min_frequency=2,
    special_tokens=["<|endoftext|>", "<DOCNO>", "</DOCNO>"]
)

tokenizer.save_model(output_dir)

tokenizer = GPT2TokenizerFast.from_pretrained("telugu-tokenizer")
tokenizer.save_pretrained("telugu-gpt2-tokenizer")