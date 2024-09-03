import json
import os
from datetime import datetime


class GenerationLogger:
    def __init__(self, log_file='logs/generation_log.jsonl'):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def log(self, step, data):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'step': step,
            'data': data
        }
        with open(self.log_file, 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')

    def log_seed(self, seed):
        self.log('seed_generation', {'seed': seed})

    def log_task_description(self, seed, description, invocation):
        self.log('task_description_generation', {
            'seed': seed,
            'description': description,
            'invocation': invocation
        })

    def log_command(self, invocation, command):
        self.log('command_generation', {
            'invocation': invocation,
            'command': command
        })

    def log_graph_update(self, invocation, command):
        self.log('graph_update', {
            'invocation': invocation,
            'command': command
        })


logger = GenerationLogger()
