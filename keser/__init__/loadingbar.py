import time
import sys
from datetime import datetime

class LoadingBar:
    def __init__(self, total, desc="", ncols=100):
        self.total = total
        self.desc = desc
        self.ncols = ncols
        self.current = 0
        self.start_time = time.time()
        self.last_update = 0
        self.update_interval = 0.1  # Update every 100ms
        self.found = 0
        self.speed = 0
        self.eta = 0
        self.progress = 0
        self.bar_length = 0
        self.bar = ""
        self.empty = ""
        self.status = ""
        print(f"\n\033[38;2;255;255;255m[{yellow('INF')}\033[38;2;255;255;255m] {yellow('Initializing search')} \033[38;2;255;255;255m{desc}\n")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def update(self, n=1, found=0):
        self.current += n
        self.found += found
        current_time = time.time()
        
        if current_time - self.last_update < self.update_interval:
            return
            
        self.last_update = current_time
        elapsed = current_time - self.start_time
        self.speed = self.current / elapsed if elapsed > 0 else 0
        self.eta = (self.total - self.current) / self.speed if self.speed > 0 else 0
        
        # Calculate progress percentage
        self.progress = self.current / self.total
        self.bar_length = int(self.progress * self.ncols)
        
        # Create gradient colors for the bar
        self.bar = ""
        for i in range(self.bar_length):
            ratio = i / self.bar_length if self.bar_length > 0 else 0
            r = int(255 * (1 - ratio))
            g = int(255)
            b = int(0)
            self.bar += f"\033[38;2;{r};{g};{b}m█\033[0m"
        
        # Create empty space
        self.empty = " " * (self.ncols - self.bar_length)
        
        # Format the status line
        self.status = f"\r{self.desc} |{self.bar}{self.empty}| ▇▇▅ {self.current}/{self.total} [{int(self.progress*100)}%] in {int(elapsed)}s (~{int(self.eta)}s, {self.speed:.1f}/s)"
        
        sys.stdout.write(self.status)
        sys.stdout.flush()

    def close(self):
        sys.stdout.write("\n")
        sys.stdout.flush()

def yellow(text):
    gradient_output = ""
    start_color = (255, 255, 0)
    end_color = (0, 255, 0)

    for i, char in enumerate(text):
        ratio = i / len(text)
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        gradient_output += f"\033[38;2;{r};{g};{b}m{char}"

    return gradient_output + "\033[0m" 