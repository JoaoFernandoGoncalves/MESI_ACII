class RAM:
    def __init__(self, size):
        self.data = {i: {"name": f"Name{i}", "phone": f"123-456-78{i}"} for i in range(size)}

    def print_ram(self):
        return "\n".join(f"Address: {address}, Data: {content}" for address, content in self.data.items())
