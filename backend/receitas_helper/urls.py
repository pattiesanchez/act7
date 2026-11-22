from django.urls import path
from .views import *

urlpatterns = [
    path('receitas/editar/foto', Classe1.as_view()),
    path('receitas/slug/<str:slug>', Classe2.as_view()),
    path('receitas-home', Classe3.as_view()),
    path('receitas-painel/<int:id>', Classe4.as_view()),
    path('receitas-pesquisa', Classe5.as_view()),
]