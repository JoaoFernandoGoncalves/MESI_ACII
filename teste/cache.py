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
            # Encontra o índice da linha mais antiga
            oldest_tag = self.order.pop(0)
            for idx, line in enumerate(self.cache):
                if line.tag == oldest_tag:
                    # Substitui a linha mais antiga
                    self.cache[idx] = CacheLine(tag=tag, data=data, state='E')
                    self.order.append(tag)
                    return self.cache[idx]
        else:
            # Se ainda não atingiu a capacidade máxima, adicione a nova linha
            for idx, line in enumerate(self.cache):
                if line.tag is None:  # Encontra uma linha vazia
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
