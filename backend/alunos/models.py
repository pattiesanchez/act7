from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    foto = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    
class Plano(models.Model):
    nome = models.CharField(max_length=100)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duracao_dias = models.IntegerField()

    def __str__(self):
        return self.nome
    
class Matricula(models.Model):

    STATUS = (
        ('ATIVA', 'Ativa'),
        ('VENCIDA', 'Vencida'),
        ('CANCELADA', 'Cancelada'),
    )

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE
    )

    plano = models.ForeignKey(
        Plano,
        on_delete=models.PROTECT
    )

    data_inicio = models.DateField()

    data_fim = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='ATIVA'
    )

class RegistroAcesso(models.Model):

    aluno = models.ForeignKey(
        Aluno,
        on_delete=models.CASCADE
    )

    entrada = models.DateTimeField()

    saida = models.DateTimeField(
        null=True,
        blank=True
    )

    observacao = models.TextField(
        blank=True,
        null=True
    )