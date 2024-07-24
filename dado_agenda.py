"""
Classe Pessoa define o tipo de dado que será manipulado na memória RAM e Cache
"""

class dado:
    def __init__(self, nome, telefone, endereco, aniversario):
        self.nome = nome
        self.telefone = telefone
        self. endereco = endereco
        self.aniversario = aniversario
    
    def informacoes(self):
        print(f'\nNome: {self.nome}\nTelefone: {self.telefone}\nEndereco: {self.endereco}\nAniversario: {self.aniversario}\n')

