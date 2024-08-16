import tkinter as tk
from tkinter import messagebox
from cache_operations import read_from_cache, write_to_cache
from mesi_protocol import MESIState

class Registro:
    def __init__(self, nome, telefone, endereco):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco

RAM_SIZE = 50
CACHE_SIZE = 5
NUM_PROCESSORS = 3

ram = [Registro(f"Nome{i}", f"Telefone{i}", f"Endereco{i}") for i in range(RAM_SIZE)]
caches = [{'lines': [None]*CACHE_SIZE, 'states': [MESIState.INVALID]*CACHE_SIZE} for _ in range(NUM_PROCESSORS)]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Protocolo MESI - Agenda")
        
        # Configuração da interface
        self.create_widgets()
        self.update_cache_display()

    def create_widgets(self):
        # Seção de inputs
        tk.Label(self.root, text="Processador (0 a 2):").grid(row=0, column=0)
        self.processor_id_entry = tk.Entry(self.root)
        self.processor_id_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Nome:").grid(row=1, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Telefone:").grid(row=2, column=0)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Endereço:").grid(row=3, column=0)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.grid(row=3, column=1)

        tk.Button(self.root, text="Ler Contato", command=self.read_contact).grid(row=4, column=0)
        tk.Button(self.root, text="Adicionar/Atualizar Contato", command=self.write_contact).grid(row=4, column=1)
        
        # Seção de visualização das caches
        self.cache_frames = []
        for i in range(NUM_PROCESSORS):
            frame = tk.LabelFrame(self.root, text=f"Cache P{i + 1}", padx=10, pady=10)
            frame.grid(row=5, column=i, padx=10, pady=10)
            self.cache_frames.append(frame)
    
    def update_cache_display(self):
        for i in range(NUM_PROCESSORS):
            frame = self.cache_frames[i]
            for widget in frame.winfo_children():
                widget.destroy()  # Limpa o frame antes de atualizar
            
            cache = caches[i]
            for j in range(CACHE_SIZE):
                line_content = f"Line {j}: {cache['lines'][j].nome if cache['lines'][j] else 'Vazio'} | Estado: {cache['states'][j]}"
                tk.Label(frame, text=line_content).pack()

    def read_contact(self):
        processor_id = int(self.processor_id_entry.get())
        name = self.name_entry.get()
        result = read_from_cache(processor_id, name, ram, caches)
        if result:
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, result.telefone)
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, result.endereco)
        else:
            messagebox.showinfo("Resultado", "Contato não encontrado.")
        self.update_cache_display()

    def write_contact(self):
        processor_id = int(self.processor_id_entry.get())
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        write_to_cache(processor_id, name, phone, address, ram, caches)
        self.update_cache_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
