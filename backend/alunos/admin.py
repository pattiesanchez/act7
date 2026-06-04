from django.contrib import admin

from .models import (
    Aluno,
    Plano,
    Matricula,
    RegistroAcesso
)

admin.site.register(Aluno)
admin.site.register(Plano)
admin.site.register(Matricula)
admin.site.register(RegistroAcesso)