from datetime import datetime

class Log:
    def __init__(self):
        self.entries = []

    def add_entry(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.entries.append({'Timestamp': timestamp, 'Message': message})

    def get_entries(self):
        return self.entries
