import random
from faker import Faker

fake = Faker('pt_BR')

class RAM:
    def __init__(self, size):
        self.size = size
        self.data = [self.generate_fake_data() for _ in range(size)]

    def generate_fake_data(self):
        name = fake.name()
        phone = fake.phone_number()
        address = fake.address()
        return {"name": name, "phone": phone, "address": address}

    def print_ram(self):
        return "\n".join(f"Address {i}: Name: {entry['name']}, Phone: {entry['phone']}, Address: {entry['address']}"
                         for i, entry in enumerate(self.data))
