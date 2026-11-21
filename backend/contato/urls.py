from django.urls import path
from .views import *

urlpatterns = [
    path('contato', Classe1.as_view()),
]