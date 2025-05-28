from django.db import models

class Estado(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    uf = models.CharField(max_length=2, blank=False, null=False)

    def __str__(self):
        return f'{self.nome} - {self.uf}'


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nome} - {self.estado.uf}'

class FornecedorModel(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    cnpj = models.CharField(max_length=14, blank=True, null=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=15, blank=False, null=False)
    cep = models.CharField(max_length=8, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nome} - {self.cnpj}'