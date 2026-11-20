from django.urls import path
from .views import *

urlpatterns = [
    path('receitas', Classe1.as_view()),
    path('receitas/<int:id>', Classe2.as_view())
]