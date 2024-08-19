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

    def writeback(self, tag):
        """Writes back the data from a modified cache line to RAM."""
        for line in self.cache:
            if line.tag == tag and line.state == 'M':
                address = tag
                if(len(self.ram) == tag):
                    self.ram.append(line.data)
                else:
                    self.ram[address] = line.data
                
                print(f"Writeback: Data {line.data} written back to RAM at address {address}")
                break

    def replace_line(self, tag, data, app):
        if len(self.order) >= self.size:
            oldest_tag = self.order.pop(0)
            for idx, line in enumerate(self.cache):
                if line.tag == oldest_tag:
                    if line.state == 'M':
                        self.writeback(oldest_tag)
                        app.update_ram(self.ram)
                    self.cache[idx] = CacheLine(tag=tag, data=data, state='E')
                    self.order.append(tag)
                    return self.cache[idx]
        else:
            for idx, line in enumerate(self.cache):
                if line.tag is None:
                    self.cache[idx] = CacheLine(tag=tag, data=data, state='E')
                    self.order.append(tag)
                    return self.cache[idx]

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
