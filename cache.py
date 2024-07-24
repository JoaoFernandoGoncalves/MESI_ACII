import random

class mem_cache:
    def __init__(self):
        self.tamanho = 5
        self.linha = [None] * self.tamanho
        self.tag =[None] * self.tamanho

    def mapeia_cache(self, ram, pos):
        
        cheia = False

        while not cheia:
            indice = random.randint(0, 4)

            if self.linha[indice] == None:
                self.linha[indice] = ram.dados[pos]
            else:
                cheia = True