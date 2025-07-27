from tokenizers import ByteLevelBPETokenizer
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