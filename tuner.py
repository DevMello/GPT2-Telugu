from transformers import (
    GPT2Config,
    GPT2TokenizerFast,
    GPT2LMHeadModel,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments
)
from datasets import load_dataset, concatenate_datasets

tokenizer = GPT2TokenizerFast.from_pretrained("telugu-gpt2-tokenizer")

if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '<|pad|>'})

config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    n_positions=1024,
    n_ctx=1024,
    n_embd=768,
    n_layer=12,
    n_head=12,
    bos_token_id=tokenizer.bos_token_id,
    eos_token_id=tokenizer.eos_token_id,
    pad_token_id=tokenizer.pad_token_id,
)

config.save_pretrained("telugu-gpt2-small")

books_dataset = load_dataset('text', data_files={'train': 'data/books.txt'})
news_dataset = load_dataset('text', data_files={'train': 'data/news_website_cleaned.txt'})

model = GPT2LMHeadModel(config)
model.resize_token_embeddings(len(tokenizer))
model.gradient_checkpointing_enable()

dataset = concatenate_datasets([books_dataset['train'], news_dataset['train']])

def tokenize_function(example):
    return tokenizer(example["text"], truncation=True, max_length=1024)

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=["text"])

tokenized_dataset = tokenized_dataset.filter(lambda example: len(example['input_ids']) > 0)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

training_args = TrainingArguments(
    output_dir="./telugu-gpt2-small",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    num_train_epochs=3,
    save_steps=1000,
    learning_rate=3e-5,
    fp16=True,
    gradient_checkpointing=True,
    logging_steps=100,
    save_total_limit=2,
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator,
)

trainer.train(resume_from_checkpoint=True)

trainer.save_model("telugu-gpt2-small")
tokenizer.save_pretrained("telugu-gpt2-small")
