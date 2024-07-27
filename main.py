import  ram
import cache

RAM = ram.mem_ram()

RAM.preenche_ram()
RAM.mostra_ram()

p1 = cache.mem_cache()
p2 = cache.mem_cache()
p3 = cache.mem_cache()

p1.leitura_cache(p2, p3, RAM, 0)

print(p1.linha, p1.tag)

p2.leitura_cache(p1, p3, RAM, 0)

print(p1.linha, p1.tag)
print(p2.linha, p2.tag)

