import random
import queue
import ram

class mem_cache:
    def __init__(self):
        self.tamanho = 5
        self.linha = [None] * self.tamanho
        self.tag =[None] * self.tamanho
        self.fifo = queue.Queue(self.tamanho)

    def notCheia(self):
        notCheia = False
        i = 0

        while not notCheia and i < self.tamanho:
            if self.linha[i] == None:
                notCheia = True
            else:
                i += 1

        return notCheia

    def mapeia_cache(self, RAM : ram.mem_ram , pos):
        notCheia = self.notCheia()

        solicitou = False

        if notCheia:
            while not solicitou:
                indice = random.randint(0, 4)

                if self.linha[indice] == None:

                    self.linha[indice] = RAM.dados[pos]
                    self.fifo.put(indice)

                    solicitou = True
        else:
            ##substituição
            return