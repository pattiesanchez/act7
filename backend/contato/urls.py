from django.urls import path
from .views import *

urlpatterns = [
    path('contato', Classe1.as_view()),
    # path('exemplo/<int:id>', Class_ExemploParametros.as_view()),
    # path('exemplo-upload', Class_ExemploUpload.as_view()),
]