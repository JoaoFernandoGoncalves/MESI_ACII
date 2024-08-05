import random
from collections import deque

# Definição da memória RAM
RAM_SIZE = 50
BLOCK_SIZE = 1  # Cada posição da RAM é um bloco

class CacheLine:
    def __init__(self, tag=None, state='I', data=None):
        self.tag = tag
        self.state = state
        self.data = data

class Cache:
    def __init__(self, size=5):
        self.size = size
        self.lines = {}  # Usando dicionário para a cache
        self.queue = deque()  # Para implementar FIFO

    def find_line(self, tag):
        return self.lines.get(tag, None)

    def replace_line(self, tag, data):
        if len(self.queue) == self.size:
            old_tag = self.queue.popleft()
            self.lines.pop(old_tag, None)
        line = CacheLine(tag=tag, state='M', data=data)
        self.lines[tag] = line
        self.queue.append(tag)
        return line

    def print_cache(self):
        print("Cache State:")
        for tag, line in self.lines.items():
            print(f"Tag: {tag}, State: {line.state}, Data: {line.data}")

class Processor:
    def __init__(self, id, ram):
        self.id = id
        self.cache = Cache()
        self.ram = ram

    def read(self, address):
        tag = address
        line = self.cache.find_line(tag)

        if line:
            if line.state == 'I':
                print(f"P{self.id}: RM (Read Miss) - Line Invalid")
                data = self.ram[address]
                line.state = 'S'  # Shared if it was in another cache, Exclusive otherwise
                line.data = data
                print(f"P{self.id}: Fetched from RAM, State: {line.state}")
            else:
                print(f"P{self.id}: RH (Read Hit) - Data: {line.data}, State: {line.state}")
                return line.data
        else:
            print(f"P{self.id}: RM (Read Miss) - Line not in Cache")
            data = self.ram[address]
            line = self.cache.replace_line(tag, data)
            line.state = 'S'
            print(f"P{self.id}: Fetched from RAM, State: {line.state}")
        return line.data

    def write(self, address, data):
        tag = address
        line = self.cache.find_line(tag)

        if line:
            if line.state in ['S', 'E', 'M']:
                print(f"P{self.id}: WH (Write Hit) - State: {line.state}")
                line.state = 'M'
                line.data = data
                print(f"P{self.id}: Updated Cache, State: {line.state}")
            else:
                print(f"P{self.id}: WM (Write Miss) - Line Invalid")
                line.state = 'M'
                line.data = data
                print(f"P{self.id}: Updated Cache, State: {line.state}")
        else:
            print(f"P{self.id}: WM (Write Miss) - Line not in Cache")
            line = self.cache.replace_line(tag, data)
            line.state = 'M'
            print(f"P{self.id}: Updated Cache, State: {line.state}")

    def print_status(self):
        print(f"Processor {self.id} Status:")
        self.cache.print_cache()

class RAM:
    def __init__(self, size):
        self.data = {i: {"name": f"Name{i}", "phone": f"123-456-78{i}"} for i in range(size)}

def print_processors_status(processors):
    for processor in processors:
        processor.print_status()
        print()

def main():
    ram = RAM(RAM_SIZE)
    processors = [Processor(i, ram.data) for i in range(3)]

    while True:
        print("1. Perform Operation")
        print("2. Print Processors Status")
        choice = input("Choose an option (1/2): ")

        if choice == '1':
            proc_id = int(input("Select Processor (0-2): "))
            op = input("Operation (R/W): ").upper()
            address = int(input("Address (0-49): "))
            if op == 'R':
                data = processors[proc_id].read(address)
                print(f"Data: {data}")
            elif op == 'W':
                name = input("Enter Name: ")
                phone = input("Enter Phone: ")
                data = {"name": name, "phone": phone}
                processors[proc_id].write(address, data)
            else:
                print("Invalid Operation")
        elif choice == '2':
            print_processors_status(processors)
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()
