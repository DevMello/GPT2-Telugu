from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset, concatenate_datasets


model = GPT2LMHeadModel.from_pretrained('gpt2')

# Load datasets from text files
books_dataset = load_dataset('text', data_files={'train': 'data/books.txt'})
news_dataset = load_dataset('text', data_files={'train': 'data/news_website.txt'})
