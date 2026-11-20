from django.urls import path
from .views import *

urlpatterns = [
    path('categorias', Classe1.as_view()),
    path('categorias/<int:id>', Classe2.as_view())
]