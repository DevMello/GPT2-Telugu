from transformers import GPT2Config, GPT2TokenizerFast, GPT2LMHeadModel, DataCollatorForLanguageModeling, Trainer, TrainingArguments
from datasets import load_dataset, concatenate_datasets

tokenizer = GPT2TokenizerFast.from_pretrained("telugu-gpt2-tokenizer")

config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    n_positions=1024,
    n_ctx=1024,
    n_embd=768,
    n_layer=12,
    n_head=12,
    bos_token_id=None,
    eos_token_id=None,
    pad_token_id=None,
)

config.save_pretrained("telugu-gpt2")


books_dataset = load_dataset('text', data_files={'train': 'data/books.txt'})
news_dataset = load_dataset('text', data_files={'train': 'data/news_website_cleaned.txt'})

model = GPT2LMHeadModel(config)
model.save_pretrained("telugu-gpt2")

# Concatenate datasets
dataset = concatenate_datasets([books_dataset['train'], news_dataset['train']])

def tokenize_function(example):
    return tokenizer(example["text"], truncation=True, max_length=1024)

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)
