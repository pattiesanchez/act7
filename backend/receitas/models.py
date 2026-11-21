from django.db import models
from autoslug import AutoSlugField
from categorias.models import Categoria

# Create your models here.

class Receita(models.Model):
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING)
    nome = models.CharField(max_length=100, null=False)
    slug = AutoSlugField(populate_from='nome', unique=True, null=False)
    tempo = models.CharField(max_length=100, null=False)
    foto = models.CharField(max_length=100, null=False)
    descricao = models.TextField()
    data = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'receitas'
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'