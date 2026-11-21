from django.urls import path
from .views import *

urlpatterns = [
    path('seguranca/registro', Classe1.as_view()),
]