import random
import queue
import ram

class mem_cache:
    def __init__(self):
        self.tamanho = 5
        self.linha = [None] * self.tamanho
        self.tag =[[None] * self.tamanho]
        self.fifo = queue.Queue(self.tamanho)

    '''def preenche_cache(self):
        for i in range(5):
            self.linha[i] = random.randint(0,5)'''

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
        blocoEmCache, posLinha = blocoEmCache(pos)

        solicitou = False

        if blocoEmCache:
            #Read_HIT   
        else:
            #READ_MISS
            return
        
    def blocoEmCache(self, pos):

        emCache = False

        for i in range(self.tamanho):
            if self.tag[i][2] == pos:
                return emCache == True, i
            else:
                return emCache
            
    def READ_HIT(self, posLinha, posBloco, RAM : ram.mem_ram,):

        if self.linha[posLinha] == RAM.dados[posBloco]:
            print("Read Hit")
            return 1
        
    def READ_MISS(self, cache2, cache3, posBloco, posLinha):

        emCache2, pos_cache2 = cache2.blocoEmCache(posBloco)
        emCache3, pos_cache3 = cache3.blocoEmCache(posBloco)


        if emCache2 or emCache3:
            if self.linha[posLinha] == cache2.linha[pos_cache2]:
                self.tag[posLinha][1] == "shared"
                cache2.tag[pos_cache2][1] == "shared"

            if self.linha[posLinha] == cache3.linha[pos_cache3]:
                self.tag[posLinha][1] == "shared"
                cache3.tag[pos_cache3][1] == "shared"
        else:
            self.tag[posLinha][1] = "exclusive"







        


