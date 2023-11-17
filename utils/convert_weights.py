import torch
import numpy as np
from transformers import T5ForConditionalGeneration, T5Tokenizer


def save_model_and_weights(model_path, pt_output_path):
    # Load model
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    # Save the model in .pt format
    torch.save(model.state_dict(), pt_output_path)


# Define the paths
model_path = 'model'  # Adjust this path to your model's directory
pt_output_path = 'model/t5_model.pt'

# Perform the conversion
save_model_and_weights(model_path, pt_output_path)
