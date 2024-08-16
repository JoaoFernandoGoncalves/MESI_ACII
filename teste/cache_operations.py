# cache_operations.py

from mesi_protocol import set_state_on_read, set_state_on_write, MESIState

def map_to_cache(address, cache_size):
    return address % cache_size

def read_from_cache(processor_id, name, ram, cache):
    for i, registro in enumerate(cache[processor_id]['lines']):
        if registro and registro.nome == name:
            print(f"RH - {name} encontrado na cache P{processor_id + 1}")
            return registro
    
    # Miss
    print(f"RM - {name} não encontrado na cache P{processor_id + 1}")
    for i, registro in enumerate(ram):
        if registro.nome == name:
            line = map_to_cache(i, len(cache[processor_id]['lines']))
            is_shared = any(cache[i]['states'][line] == MESIState.SHARED for i in range(len(cache)))
            set_state_on_read(cache, processor_id, line, is_shared)
            cache[processor_id]['lines'][line] = registro
            return registro
    print(f"{name} não encontrado na agenda.")
    return None

def write_to_cache(processor_id, name, telefone, endereco, ram, cache):
    for i, registro in enumerate(ram):
        if registro.nome == name:
            registro.telefone = telefone
            registro.endereco = endereco
            
            line = map_to_cache(i, len(cache[processor_id]['lines']))
            cache[processor_id]['lines'][line] = registro
            set_state_on_write(cache, processor_id, line)
            print(f"WH - {name} atualizado na cache P{processor_id + 1}")
            return
    
    novo_registro = Registro(name, telefone, endereco)
    ram.append(novo_registro)
    line = map_to_cache(len(ram) - 1, len(cache[processor_id]['lines']))
    cache[processor_id]['lines'][line] = novo_registro
    set_state_on_write(cache, processor_id, line)
    print(f"WM - {name} adicionado à cache P{processor_id + 1}")
