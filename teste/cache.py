import random
class CacheLine:
    def __init__(self, tag=None, data=None, state='I'):
        self.tag = tag
        self.data = data
        self.state = state

class Cache:
    def __init__(self, ram, size=5):
        self.size = size
        self.ram = ram
        self.cache = [CacheLine() for _ in range(size)]
        self.order = []  # To track the order for FIFO

    def find_line(self, tag):
        for line in self.cache:
            if line.tag == tag:
                return line
        return None

    def replace_line(self, tag, data):
        if len(self.order) >= self.size:
            oldest_tag = self.order.pop(0)
            # Invalidate the oldest line
            self.cache[self.order.index(oldest_tag)].state = 'I'

        index = len(self.order) % self.size
        self.cache[index] = CacheLine(tag=tag, data=data, state='E')
        self.order.append(tag)
        return self.cache[index]

    def clear_cache(self):
        for line in self.cache:
            line.tag = None
            line.data = None
            line.state = 'I'
        self.order.clear()

    def print_cache(self):
        cache_status = "Cache State:\n"
        for idx, line in enumerate(self.cache):
            cache_status += f"Line {idx}: Tag: {line.tag}, Data: {line.data}, State: {line.state}\n"
        return cache_status
