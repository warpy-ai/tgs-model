import torch
import numpy as np
from transformers import T5ForConditionalGeneration


def save_model_to_npz(model_path, output_file):
    # Load the fine-tuned T5 model
    model = T5ForConditionalGeneration.from_pretrained(model_path)

    # Extract model weights and convert them to NumPy arrays
    state_dict = model.state_dict()
    np_arrays = {k: v.cpu().numpy() for k, v in state_dict.items()}

    # Save the weights as a .npz file
    np.savez(output_file, **np_arrays)

    # Verifying the saved file
    loaded_npz = np.load(output_file)
    print("Saved model weights in the .npz file:")
    print(loaded_npz.files)


# Set the path to your fine-tuned model and the desired output file name
model_path = 'model'  # Replace with the path to your model directory
output_file = 'model/model_weights.npz'

# Save the model
save_model_to_npz(model_path, output_file)
