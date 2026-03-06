import sys
import time
import threading
from typing import List

class Inihandler:
    """Manager class for handling concurrent operations."""
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.workers: List[threading.Thread] = []
        self._lock = threading.Lock()
        self.is_running = False
        
    def start(self):
        """Start the manager pool."""
        with self._lock:
            if self.is_running:
                return
            self.is_running = True
            
        for i in range(self.max_workers):
            t = threading.Thread(target=self._worker_loop, name=f"Worker-{i}")
            t.daemon = True
            self.workers.append(t)
            t.start()
            
    def stop(self):
        """Stop all workers."""
        self.is_running = False
        for t in self.workers:
            t.join(timeout=2.0)
            
    def _worker_loop(self):
        """Main worker loop."""
        while self.is_running:
            time.sleep(0.1)
