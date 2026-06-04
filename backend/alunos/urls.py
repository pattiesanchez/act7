from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AlunoViewSet,
    PlanoViewSet,
    MatriculaViewSet,
    RegistroAcessoViewSet,
)

router = DefaultRouter()

router.register(
    r'alunos',
    AlunoViewSet,
    basename='aluno'
)

router.register(
    r'planos',
    PlanoViewSet,
    basename='plano'
)

router.register(
    r'matriculas',
    MatriculaViewSet,
    basename='matricula'
)

router.register(
    r'acessos',
    RegistroAcessoViewSet,
    basename='acesso'
)

urlpatterns = [
    path('', include(router.urls)),
]