import dado_agenda
import random

class mem_ram:
    #Define atributos da classe ram
    def __init__(self):
        self.tamanho = 50
        self.dados = [None] * self.tamanho

    def mostra_ram(self):
        print(self.dados)

    def dado_ram(self, pos):
        return self.dados[pos]
    
    #teste, deletar!
    def preenche_ram(self): 
        for x in range (self.tamanho):
            self.dados[x] = random.randint(0, 10)
    