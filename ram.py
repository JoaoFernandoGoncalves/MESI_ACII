import dado_agenda

class mem_ram:
    #Define atributos da classe ram
    def __init__(self):
        self.tamanho = 50
        self.dados = [None] * self.tamanho

    def mostra_ram(self):
        print(self.dados)

    def dado_ram(self, pos):
        return self.dados[pos]
    

memoria = mem_ram()
p1 = dado_agenda.dado("AAAA", "93493284", "Rua tal", "123322")
memoria.dados[10] = p1

x = memoria.leitura_ram(10)
x.informacoes()