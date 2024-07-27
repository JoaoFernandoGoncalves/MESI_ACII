import random
import queue
import ram

class mem_cache:
    def __init__(self):
        self.tamanho = 5
        self.linha = [None] * self.tamanho
        self.tag =[[None, None] for i in range (self.tamanho)]
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
 
    def leitura_cache(self, cache2, cache3, RAM : ram.mem_ram , posBloco):
        cacheNotCheia = self.notCheia()

        achouNaCache, posLinha = self.blocoEmCache(posBloco)

        solicitou = False

        if achouNaCache == True:
            self.READ_HIT(posLinha, posBloco, RAM)   
        else:
            #READ_MISS
            if cacheNotCheia:
                while not solicitou:
                    posLinha = random.randint(0, 4)
                    
                    if self.linha[posLinha] == None:
                        self.READ_MISS(cache2, cache3, posBloco, posLinha, RAM)
                        solicitou = True
            else:
                #FIFO
                return
        
    def blocoEmCache(self, pos):

        emCache = False
        tag_linha = None
        
        for i in range (self.tamanho):
            if self.tag[i][1] == pos:
                emCache = True
                tag_linha = i
        
        return emCache, tag_linha
        
    def READ_HIT(self, posLinha, posBloco, RAM : ram.mem_ram,):

        if self.linha[posLinha] == RAM.dados[posBloco]:
            print("Read Hit")
            return 1
        
    def READ_MISS(self, cache2, cache3, posBloco, posLinha, RAM : ram.mem_ram):

        self.linha[posLinha] = RAM.dados[posBloco]
        self.tag[posLinha][1] = posBloco
        print("Read Miss!")

        emCache2, pos_cache2 = cache2.blocoEmCache(posBloco)
        emCache3, pos_cache3 = cache3.blocoEmCache(posBloco)


        if emCache2 or emCache3:
            if self.linha[posLinha] == cache2.linha[pos_cache2]:
                self.tag[posLinha][0] = "shared"
                cache2.tag[pos_cache2][0] = "shared"
            elif self.linha[posLinha] == cache3.linha[pos_cache3]:
                self.tag[posLinha][0] = "shared"
                cache3.tag[pos_cache3][0] = "shared"
        else:
            self.tag[posLinha][0] = "exclusive"







        


