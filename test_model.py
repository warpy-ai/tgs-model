import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import json
import random


class NL2BashModel:
    def __init__(self, model_path):
        self.model = T5ForConditionalGeneration.from_pretrained(model_path)
        self.tokenizer = T5Tokenizer.from_pretrained(model_path)
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def generate_answer(self, question, max_length=50):
        self.model.eval()
        input_ids = self.tokenizer.encode(
            question, return_tensors='pt').to(self.device)
        output = self.model.generate(input_ids, max_length=max_length)
        answer = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return answer


def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def main():
    # Load the model
    model_path = "model"  # Replace with your model directory
    model = NL2BashModel(model_path)

    data = load_data('data/nl2bash-data.json')

    random_key = random.choice(list(data.keys()))

    # Test the model with a question
    question = data[random_key]['invocation']
    answer = model.generate_answer(question)
    print(f"Question: {question}")
    print(f"Data cmd: {data[random_key]['cmd']}")
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
