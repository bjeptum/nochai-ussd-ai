# fine_tune.py (Run in Colab; ~2-3 hours)
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset
import pandas as pd

# 1. Load Dataset (example: load Swahili news/dialogues)
dataset = load_dataset("masakhane/swahili_news", split="train[:1000]")  # Small subset
def format_data(example):
    return {"text": f"Prompt: Eleza jinsi ya kukataa rushwa. Response: {example['text'][:200]}"}  # Custom anti-corruption format
dataset = dataset.map(format_data)

# Tokenize
tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b")
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

def tokenize(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize, batched=True)
tokenized_dataset = tokenized_dataset.train_test_split(test_size=0.1)

# 2. Load Model
model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b", torch_dtype=torch.bfloat16)
model.gradient_checkpointing_enable()  # Memory save

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# 3. Training Args (Low-Resource)
training_args = TrainingArguments(
    output_dir="./swahili_gemma_finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=2,  # Small
    gradient_accumulation_steps=16,  # Simulate batch=32
    learning_rate=2e-4,
    fp16=True,  # Mixed precision
    save_steps=500,
    logging_steps=100,
    evaluation_strategy="steps",
    eval_steps=500,
    report_to=None  # Skip wandb
)

# 4. Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    data_collator=data_collator,
    tokenizer=tokenizer
)
trainer.train()

# 5. Save & Push to HF (optional)
model.save_pretrained("./swahili_gemma_finetuned")
tokenizer.save_pretrained("./swahili_gemma_finetuned")
# Then: model.push_to_hub("your-hf-username/swahili-kitu-haina")  # With login