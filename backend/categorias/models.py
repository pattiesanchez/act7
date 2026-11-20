from django.db import models
from autoslug import AutoSlugField

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=100, null=False)
    slug = AutoSlugField(populate_from='nome', unique=True, null=False)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'