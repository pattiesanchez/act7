from rest_framework import serializers
from .models import *
from dotenv import load_dotenv
import os 

load_dotenv()

class ReceitaSerializer(serializers.ModelSerializer):

    categoria = serializers.ReadOnlyField(source='categoria.nome') #além do ReadOnlyField, pode-se usar o CharField
    fecha = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", read_only=True) #formato de data e hora: 20/11/2026 04:30:00
    imagem =  serializers.SerializerMethodField() #campo personalizado para retornar a URL completa da imagem

    class Meta:
        model = Receita
        fields = ('id', 'categoria', 'nome', 'slug', 'tempo', 'foto', 'descricao', 'fecha', 'categoria', 'imagem')

    def get_imagem(self, obj):
        return f"{os.getenv('BASE_URL')}/uploads/receitas/{obj.foto}"

