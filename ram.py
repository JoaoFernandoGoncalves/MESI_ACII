import pessoa #tirar depois

"""
A memória RAM do nosso projeto é a classe ram, que basicamente é uma tabela hash
na classe temos os metódos fc_hash, insere e busca.
"""
class ram:
    #Define atributos da classe ram
    def __init__(self):
        self.tamanho = 50
        self.id = [None] * self.tamanho
        self.dados = [None] * self.tamanho

    #Função para encontra posição na ram
    def fc_hash(self, chave, tamanho):
        return chave % tamanho
    
    def insere(self, chave, dado):
        tam = len(self.id)

        pos = self.fc_hash(chave, tam)
        
        if self.id[pos] == None:
            self.id[pos] = chave
            self.dados[pos] = dado
        else:
            if self.id[pos] == chave:
                self.dados[pos] = dado
            else:
                prox_pos = self.fc_hash(pos + 1, len(self.id))

                while self.id[prox_pos] != None and self.id[prox_pos] != chave:
                    prox_pos = self.fc_hash(prox_pos + 1, len(self.id))
                
                if self.id[prox_pos] == None:
                    self.id[prox_pos] = chave
                    self.dados[prox_pos] = dado
                else:
                    self.dados[prox_pos] = dado
    
    def remove(self, chave):
        tam = len(self.id)

        pos_inicial = self.fc_hash(chave, tam)

        dado = None
        encontrou = False
        pos = pos_inicial

        while self.id[pos] != None and not encontrou:

            if self.id[pos] == chave:
                encontrou = True

                self.id[pos] = None
                self.dados[pos] = None
            else:
                pos = self.fc_hash(pos + 1, tam)

                if pos == pos_inicial:
                    break
    
    def busca(self, chave):
        tam = len(self.id)

        pos_inicial = self.fc_hash(chave, tam)

        dado = None
        encontrou = False
        pos = pos_inicial

        while self.id[pos] != None and not encontrou:

            if self.id[pos] == chave:
                encontrou = True

                dado = self.dados[pos]
            else:
                pos = self.fc_hash(pos + 1, tam)
                
                if pos == pos_inicial:
                    break
        
        return dado
    
    
#Testes

memoria = ram()

x = pessoa.Pessoa("Joao", "44999310433", "Rua seila", "19/09/2002")

memoria.insere(95, x)

print(memoria.id)

dado : pessoa.Pessoa = memoria.busca(95)

dado.informacoes()

memoria.remove(95)

print(memoria.id)
print(memoria.dados)