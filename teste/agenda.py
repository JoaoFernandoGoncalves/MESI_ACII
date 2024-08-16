import tkinter as tk
from tkinter import messagebox, ttk
from ram import RAM
from cache import Cache
from log import Log

RAM_SIZE = 50

class Processor:
    def __init__(self, id, ram, log):
        self.id = id
        self.cache = Cache(ram=ram.data)
        self.ram = ram
        self.log = log

    def read(self, address):
        tag = address
        line = self.cache.find_line(tag)
        if line:
            if line.state == 'I':
                data = self.ram.data[address]
                line.state = 'S'
                line.data = data
                message = f"Processor {self.id}: Read Miss - Data fetched from RAM. New State: {line.state}\nData: {data}"
            else:
                message = f"Processor {self.id}: Read Hit - Data: {line.data}. State: {line.state}"
        else:
            data = self.ram.data[address]
            line = self.cache.replace_line(tag, data)
            line.state = 'S'
            message = f"Processor {self.id}: Read Miss - Data fetched from RAM. New State: {line.state}\nData: {data}"
        
        self.log.add_entry(message)
        return message

    def write(self, address, data):
        tag = address
        line = self.cache.find_line(tag)
        if line:
            if line.state in ['S', 'E', 'M']:
                line.state = 'M'
                line.data = data
                message = f"Processor {self.id}: Write Hit - Data updated in cache. New State: {line.state}\nData: {data}"
            else:
                line.state = 'M'
                line.data = data
                message = f"Processor {self.id}: Write Miss - Data updated in cache. New State: {line.state}\nData: {data}"
        else:
            line = self.cache.replace_line(tag, data)
            line.state = 'M'
            message = f"Processor {self.id}: Write Miss - Data added to cache. New State: {line.state}\nData: {data}"
        
        self.log.add_entry(message)
        return message

class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Pessoal")
        self.geometry("800x600")

        self.ram = RAM(RAM_SIZE)
        self.log = Log()
        self.processors = [Processor(i, self.ram, self.log) for i in range(3)]

        self.create_widgets()

    def create_widgets(self):
        # Treeview for contacts
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Phone", "Address"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Address", text="Address")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Buttons
        self.add_button = tk.Button(self, text="Add Contact", command=self.add_contact)
        self.add_button.pack(side=tk.LEFT)

        self.edit_button = tk.Button(self, text="Edit Contact", command=self.edit_contact)
        self.edit_button.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack(side=tk.LEFT)

        self.show_status_button = tk.Button(self, text="Show Status", command=self.show_status)
        self.show_status_button.pack(side=tk.LEFT)

        self.show_log_button = tk.Button(self, text="Show Log", command=self.show_log)
        self.show_log_button.pack(side=tk.LEFT)

        # Processor selection
        self.processor_var = tk.IntVar(value=0)
        self.processor_select = ttk.Combobox(self, textvariable=self.processor_var, values=[f"Processor {i}" for i in range(3)], state="readonly")
        self.processor_select.pack(side=tk.LEFT)

        # Bind processor selection change
        self.processor_select.bind("<<ComboboxSelected>>", self.update_cache_display)

        self.load_ram_to_tree()

    def load_ram_to_tree(self):
        self.tree.delete(*self.tree.get_children())  # Clear existing entries
        for idx, entry in enumerate(self.ram.data):
            self.tree.insert("", tk.END, iid=idx, values=(idx, entry['name'], entry['phone'], entry['address']))

    def add_contact(self):
        self._open_contact_window("Add")

    def edit_contact(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Edit Contact", "Select a contact to edit.")
            return
        item_id = selected_item[0]
        self._open_contact_window("Edit", item_id)

    def delete_contact(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Delete Contact", "Select a contact to delete.")
            return
        item_id = selected_item[0]
        if 0 <= int(item_id) < len(self.ram.data):
            del self.ram.data[int(item_id)]
            self.load_ram_to_tree()
            self.update_cache()
        else:
            messagebox.showwarning("Delete Contact", "Invalid contact ID.")

    def _open_contact_window(self, mode, item_id=None):
        contact_window = tk.Toplevel(self)
        contact_window.title(f"{mode} Contact")

        tk.Label(contact_window, text="Name:").grid(row=0, column=0)
        tk.Label(contact_window, text="Phone:").grid(row=1, column=0)
        tk.Label(contact_window, text="Address:").grid(row=2, column=0)

        self.name_entry = tk.Entry(contact_window)
        self.phone_entry = tk.Entry(contact_window)
        self.address_entry = tk.Entry(contact_window)

        self.name_entry.grid(row=0, column=1)
        self.phone_entry.grid(row=1, column=1)
        self.address_entry.grid(row=2, column=1)

        if mode == "Edit":
            contact = self.ram.data[int(item_id)]
            self.name_entry.insert(0, contact['name'])
            self.phone_entry.insert(0, contact['phone'])
            self.address_entry.insert(0, contact['address'])

        tk.Button(contact_window, text=f"{mode}", command=lambda: self.save_contact(mode, item_id, contact_window)).grid(row=3, column=1)

    def save_contact(self, mode, item_id=None, contact_window=None):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        if mode == "Add":
            self.ram.data.append({"name": name, "phone": phone, "address": address})
            self.tree.insert("", tk.END, iid=len(self.ram.data)-1, values=(len(self.ram.data)-1, name, phone, address))
        elif mode == "Edit":
            self.ram.data[int(item_id)] = {"name": name, "phone": phone, "address": address}
            self.tree.item(item_id, values=(item_id, name, phone, address))
        
        self.update_cache()
        if contact_window:
            contact_window.destroy()

    def update_cache(self):
        selected_processor_id = self.processor_var.get()
        processor = self.processors[selected_processor_id]
        # Clear cache before updating
        processor.cache.clear_cache()
        # Update cache only for relevant items
        for idx, entry in enumerate(self.ram.data):
            processor.write(idx, entry)

    def update_cache_display(self, event=None):
        selected_processor_id = self.processor_var.get()
        processor = self.processors[selected_processor_id]

        if hasattr(self, 'cache_window'):
            self.cache_window.destroy()

        self.cache_window = tk.Toplevel(self)
        self.cache_window.title(f"Cache for Processor {selected_processor_id}")

        cache_text = tk.Text(self.cache_window, height=10, width=80, wrap='none')
        cache_text.pack()

        cache_status = processor.cache.print_cache()
        cache_text.insert(tk.END, cache_status)

    def show_status(self):
        self.status_window = tk.Toplevel(self)
        self.status_window.title("Simulation Status")

        tk.Label(self.status_window, text="RAM Status:").pack()
        ram_status_text = tk.Text(self.status_window, height=10, width=80, wrap='none')
        ram_status_text.pack()

        tk.Label(self.status_window, text="Cache Status:").pack()
        cache_status_text = tk.Text(self.status_window, height=10, width=80, wrap='none')
        cache_status_text.pack()

        ram_status = "\n".join(f"ID: {idx}, Name: {entry['name']}, Phone: {entry['phone']}, Address: {entry['address']}" for idx, entry in enumerate(self.ram.data))
        cache_status = "\n".join(f"Processor {proc.id} Cache:\n{proc.cache.print_cache()}" for proc in self.processors)

        ram_status_text.insert(tk.END, ram_status)
        cache_status_text.insert(tk.END, cache_status)

    def show_log(self):
        self.log_window = tk.Toplevel(self)
        self.log_window.title("Log")

        log_tree = ttk.Treeview(self.log_window, columns=("Time", "Processor", "Operation", "Details"), show='headings')
        log_tree.heading("Time", text="Time")
        log_tree.heading("Processor", text="Processor")
        log_tree.heading("Operation", text="Operation")
        log_tree.heading("Details", text="Details")
        log_tree.pack(fill=tk.BOTH, expand=True)

        for entry in self.log.get_entries():
            log_tree.insert("", tk.END, values=entry)

if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()
