import torch
from transformers import T5ForConditionalGeneration
from transformers import T5Tokenizer


# Replace "t5-small" with the appropriate model size you fine-tuned
model = T5ForConditionalGeneration.from_pretrained("model")

weights = torch.load("model/pytorch_model.pt")
model.load_state_dict(weights)

state_dict = model.state_dict()

torch.save(state_dict, "model/pytorch_model.ot")
