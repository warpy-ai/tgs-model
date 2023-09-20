from transformers import T5ForConditionalGeneration, T5Tokenizer, TextDataset, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, Seq2SeqTrainer
import torch

# Initialize the T5 base model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("model")
tokenizer = T5Tokenizer.from_pretrained("t5-small")

# Move model to device
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)

# Test the model on a sample input text
sample_input_text = "Display current running kernel's compile-time config file."
input_tokenized = tokenizer.encode_plus(
    sample_input_text,
    max_length=512,
    padding='max_length',
    truncation=True,
    return_tensors="pt"
)

# Move to device
input_tokenized.to(device)

# Generate output
output_ids = model.generate(
    input_ids=input_tokenized["input_ids"].to(device),
    attention_mask=input_tokenized["attention_mask"].to(device),
    max_length=50,
    min_length=5,
    temperature=1.0
)

# Decode and print the output
decoded_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print("Generated Output:", decoded_output)
