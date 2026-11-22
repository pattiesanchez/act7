from django.urls import path
from .views import *

urlpatterns = [
    path('seguranca/registro', Classe1.as_view()),
    path('seguranca/verificacao/<str:token>', Classe2.as_view()),
    path('seguranca/login', Classe3.as_view()),
]