import time
from collections import deque

class TokenBucket:
    def __init__(self, rate: int, per_seconds: float):
        self.rate = rate
        self.per = per_seconds
        self.tokens = deque()

    def allow(self) -> bool:
        now = time.time()
        while self.tokens and now - self.tokens[0] > self.per:
            self.tokens.popleft()
        if len(self.tokens) < self.rate:
            self.tokens.append(now)
            return True
        return False
