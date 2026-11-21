from rest_framework.views import APIView
from .models import *
from django.http.response import JsonResponse
from http import HTTPStatus
from django.utils import timezone
#chamada do modulo utilidades
from utilidades import utilidades 

# Create your views here.

class Classe1(APIView): 

    def post(self, request): 
        if request.data.get('nome')==None or not request.data['nome']:
            return JsonResponse({"error":"O campo nome é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('email')==None or not request.data['email']:
            return JsonResponse({"error":"O campo email é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('telefone')==None or not request.data['telefone']:
            return JsonResponse({"error":"O campo telefone é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('mensagem')==None or not request.data['mensagem']:
            return JsonResponse({"error":"O campo mensagem é obrigatório"}, status=HTTPStatus.BAD_REQUEST)

        try:
            Contato.objects.create(nome=request.data['nome'], email=request.data['email'], telefone=request.data['telefone'], mensagem=request.data['mensagem'], data=timezone.now())
        except Exception as e:
            return JsonResponse({"error":"Erro inesperado"}, status=HTTPStatus.BAD_REQUEST)
        return JsonResponse({"success":"Registro criado com sucesso"}, status=HTTPStatus.OK)