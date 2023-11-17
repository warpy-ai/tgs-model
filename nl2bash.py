from torch.utils.data import Dataset
import torch
_CITATION = """\
@inproceedings{LinWZE2018:NL2Bash, 
  author = {Xi Victoria Lin and Chenglong Wang and Luke Zettlemoyer and Michael D. Ernst}, 
  title = {NL2Bash: A Corpus and Semantic Parser for Natural Language Interface to the Linux Operating System}, 
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources
               and Evaluation {LREC} 2018, Miyazaki (Japan), 7-12 May, 2018.},
  year = {2018} 
}
"""

_DESCRIPTION = """\
The dataset is constructed from
https://github.com/TellinaTool/nl2bash
"""


class CommandDataset(Dataset):
    def __init__(self, data, tokenizer, source_max_token_len, target_max_token_len):
        self.data = data
        self.tokenizer = tokenizer
        self.source_max_token_len = source_max_token_len
        self.target_max_token_len = target_max_token_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        parts = item.split('</s>')
        source_text = parts[0].strip()  # Command description
        target_text = parts[1].strip()  # Actual command

        tokenized_input = self.tokenizer.encode_plus(
            source_text,
            max_length=self.source_max_token_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        tokenized_target = self.tokenizer.encode_plus(
            target_text,
            max_length=self.target_max_token_len,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        return {
            "input_ids": tokenized_input['input_ids'].squeeze(0),
            "attention_mask": tokenized_input['attention_mask'].squeeze(0),
            "labels": tokenized_target['input_ids'].squeeze(0)
        }
