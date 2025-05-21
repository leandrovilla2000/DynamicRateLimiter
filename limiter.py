import time
from threading import Lock

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity                
        self.refill_rate = refill_rate          # Tokens/Second
        self.tokens = capacity                  # Available tokens
        self.last_checked = time.time()         
        self.lock = Lock()                      

    def consume(self, tokens=1):
        with self.lock: # controls the concurrency
            now = time.time()
            elapsed = now - self.last_checked

            # Refill tokens till capacity
            refill = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + refill)
            print(f"Tokens refilled to {self.tokens}\n")
            self.last_checked = now

            # Consumes tokens 
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False
