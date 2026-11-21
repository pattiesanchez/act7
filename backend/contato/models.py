from django.db import models

# Create your models here.

class Contato(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=True)
    email = models.CharField(max_length=100, null=False, blank=True)
    telefone = models.CharField(max_length=100, null=False, blank=True)
    mensagem = models.TextField()
    data = models.DateTimeField()

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'contatos'
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'