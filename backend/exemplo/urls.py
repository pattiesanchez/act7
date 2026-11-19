from django.urls import path
from .views import Class_Exemplo, Class_ExemploParametros, Class_ExemploUpload

urlpatterns = [
    path('exemplo', Class_Exemplo.as_view()),
    path('exemplo/<int:id>', Class_ExemploParametros.as_view()),
    path('exemplo-upload', Class_ExemploUpload.as_view()),
]