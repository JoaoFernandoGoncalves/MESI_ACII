# mesi_protocol.py

class MESIState:
    MODIFIED = 'Modified'
    EXCLUSIVE = 'Exclusive'
    SHARED = 'Shared'
    INVALID = 'Invalid'

def set_state_on_read(cache, processor_id, line_index, is_shared):
    if is_shared:
        cache[processor_id]['states'][line_index] = MESIState.SHARED
    else:
        cache[processor_id]['states'][line_index] = MESIState.EXCLUSIVE

def set_state_on_write(cache, processor_id, line_index):
    cache[processor_id]['states'][line_index] = MESIState.MODIFIED
    for i in range(len(cache)):
        if i != processor_id:
            cache[i]['states'][line_index] = MESIState.INVALID
