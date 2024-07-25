import  ram
import cache

RAM = ram.mem_ram()

RAM.preenche_ram()
RAM.mostra_ram()

p1 = cache.mem_cache()
p2 = cache.mem_cache()
p2.preenche_cache()

print(p1.linha)
print(p2.linha)

p1.mapeia_cache(RAM, 5)


print(p1.linha)
print(p2.mapeia_cache(RAM, 10))
