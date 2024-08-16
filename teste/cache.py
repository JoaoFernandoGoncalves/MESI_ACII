import random
from collections import deque

class CacheLine:
    def __init__(self, tag=None, state='I', data=None):
        self.tag = tag
        self.state = state
        self.data = data

class Cache:
    def __init__(self, size=5, ram=None):
        self.size = size
        self.lines = {}
        self.queue = deque()
        self.ram = ram

    def find_line(self, tag):
        return self.lines.get(tag, None)

    def replace_line(self, tag, data):
        if len(self.queue) == self.size:
            old_tag = self.queue.popleft()
            old_line = self.lines.pop(old_tag, None)
            if old_line and old_line.state == 'M':
                print(f"Writing back modified data to RAM at address {old_tag}")
                self.ram[old_tag] = old_line.data
        line = CacheLine(tag=tag, state='M', data=data)
        self.lines[tag] = line
        self.queue.append(tag)
        return line

    def print_cache(self):
        return "\n".join(f"Tag: {tag}, State: {line.state}, Data: {line.data}" for tag, line in self.lines.items())
