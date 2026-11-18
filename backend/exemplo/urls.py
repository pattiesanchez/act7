from django.urls import path
from .views import Class_Exemplo, Class_ExemploParametros

urlpatterns = [
    path('exemplo', Class_Exemplo.as_view()),
    path('exemplo/<int:id>', Class_ExemploParametros.as_view()),
]