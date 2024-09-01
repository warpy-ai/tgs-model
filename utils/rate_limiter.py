import time
from threading import Lock


class RateLimiter:
    def __init__(self, requests_per_minute, tokens_per_minute):
        self.requests_per_minute = requests_per_minute
        self.tokens_per_minute = tokens_per_minute
        self.request_timestamps = []
        self.token_count = 0
        self.last_reset = time.time()
        self.lock = Lock()

    def wait(self, tokens):
        with self.lock:
            current_time = time.time()

            # Reset counters if a minute has passed
            if current_time - self.last_reset >= 60:
                self.request_timestamps = []
                self.token_count = 0
                self.last_reset = current_time

            # Wait if request limit is reached
            while len(self.request_timestamps) >= self.requests_per_minute:
                time.sleep(0.1)
                current_time = time.time()
                self.request_timestamps = [
                    t for t in self.request_timestamps if current_time - t < 60]

            # Wait if token limit is reached
            while self.token_count + tokens > self.tokens_per_minute:
                time.sleep(0.1)
                current_time = time.time()
                if current_time - self.last_reset >= 60:
                    self.token_count = 0
                    self.last_reset = current_time

            # Update counters
            self.request_timestamps.append(current_time)
            self.token_count += tokens


rate_limiter = RateLimiter(requests_per_minute=50, tokens_per_minute=40000)
