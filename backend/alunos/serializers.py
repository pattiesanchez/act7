from rest_framework import serializers

from .models import (
    Aluno,
    Plano,
    Matricula,
    RegistroAcesso
)


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'


class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = '__all__'


class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'


class RegistroAcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroAcesso
        fields = '__all__'