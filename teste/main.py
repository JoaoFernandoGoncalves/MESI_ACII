import tkinter as tk
from tkinter import messagebox
from cache import Cache
from ram import RAM

RAM_SIZE = 50

class Processor:
    def __init__(self, id, ram):
        self.id = id
        self.cache = Cache(ram=ram)
        self.ram = ram

    def read(self, address):
        tag = address
        line = self.cache.find_line(tag)
        if line:
            if line.state == 'I':
                data = self.ram[address]
                line.state = 'S'
                line.data = data
                return f"Read Miss - Data fetched from RAM. New State: {line.state}"
            return f"Read Hit - Data: {line.data}. State: {line.state}"
        else:
            data = self.ram[address]
            line = self.cache.replace_line(tag, data)
            line.state = 'S'
            return f"Read Miss - Data fetched from RAM. New State: {line.state}"

    def write(self, address, data):
        tag = address
        line = self.cache.find_line(tag)
        if line:
            if line.state in ['S', 'E', 'M']:
                line.state = 'M'
                line.data = data
                return f"Write Hit - Data updated in cache. New State: {line.state}"
            else:
                line.state = 'M'
                line.data = data
                return f"Write Miss - Data updated in cache. New State: {line.state}"
        else:
            line = self.cache.replace_line(tag, data)
            line.state = 'M'
            return f"Write Miss - Data added to cache. New State: {line.state}"

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MESI Protocol Simulator")
        self.geometry("600x400")

        self.ram = RAM(RAM_SIZE)
        self.processors = [Processor(i, self.ram.data) for i in range(3)]

        self.create_widgets()

    def create_widgets(self):
        self.processor_label = tk.Label(self, text="Select Processor (0-2):")
        self.processor_label.pack()

        self.processor_entry = tk.Entry(self)
        self.processor_entry.pack()

        self.operation_label = tk.Label(self, text="Operation (R/W):")
        self.operation_label.pack()

        self.operation_entry = tk.Entry(self)
        self.operation_entry.pack()

        self.address_label = tk.Label(self, text="Address (0-49):")
        self.address_label.pack()

        self.address_entry = tk.Entry(self)
        self.address_entry.pack()

        self.data_label = tk.Label(self, text="Data (for write):")
        self.data_label.pack()

        self.data_entry = tk.Entry(self)
        self.data_entry.pack()

        self.execute_button = tk.Button(self, text="Execute", command=self.execute_command)
        self.execute_button.pack()

        self.status_button = tk.Button(self, text="Print Processors Status", command=self.print_processors_status)
        self.status_button.pack()

        self.ram_button = tk.Button(self, text="Print RAM Status", command=self.print_ram_status)
        self.ram_button.pack()

    def execute_command(self):
        try:
            proc_id = int(self.processor_entry.get())
            op = self.operation_entry.get().upper()
            address = int(self.address_entry.get())
            data = self.data_entry.get()

            if op == 'R':
                result = self.processors[proc_id].read(address)
            elif op == 'W':
                if data:
                    name, phone = data.split(',')
                    data_dict = {"name": name, "phone": phone}
                    result = self.processors[proc_id].write(address, data_dict)
                else:
                    result = "No data provided for write operation."
            else:
                result = "Invalid Operation"
            
            messagebox.showinfo("Result", result)
        except ValueError as e:
            messagebox.showerror("Error", "Invalid input. Please check your entries.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def print_processors_status(self):
        status = "\n".join(f"Processor {proc.id}:\n{proc.cache.print_cache()}" for proc in self.processors)
        messagebox.showinfo("Processors Status", status)

    def print_ram_status(self):
        ram_status = self.ram.print_ram()
        messagebox.showinfo("RAM Status", ram_status)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
