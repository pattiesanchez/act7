from rest_framework.views import APIView
from .models import *
from django.http.response import JsonResponse
from rest_framework.response import Response
from .serializers import *
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from receitas.models import *

# Create your views here.

class Classe1(APIView):

    def get(self, request):
        data = Categoria.objects.order_by('-id').all()
        dados_json = CategoriaSerializer(data, many=True)
        # return Response(dados_json.data)
        return JsonResponse({"data":dados_json.data}, status=HTTPStatus.OK)

    def post(self, request):
        if request.data.get('nome')==None or not request.data.get('nome'):
            return JsonResponse({"error":"O campo nome é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        # dados_json = CategoriaSerializer(data=request.data)
        # if dados_json.is_valid():
        #     dados_json.save()
        #     return JsonResponse({"data":dados_json.data}, status=HTTPStatus.CREATED)
        # return JsonResponse({"error":dados_json.errors}, status=HTTPStatus.BAD_REQUEST)
        try: 
            Categoria.objects.create(nome=request.data['nome'])
            return JsonResponse({"estado":"ok", "mensagem":"Categoria criada com sucesso"}, status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404("Erro ao criar categoria: " + str(e))

class Classe2(APIView):

    def get(self, request, id):
        try:
            data = Categoria.objects.get(id=id)
            dados_json = CategoriaSerializer(data)
            # return Response(dados_json.data)
            return JsonResponse({"data":dados_json.data}, status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            # return JsonResponse({"error": "Categoria nao encontrada"}, status=HTTPStatus.NOT_FOUND)
            raise Http404("Categoria nao encontrada")

    def put(self, request, id):
        if request.data.get('nome')==None:
            return JsonResponse({"error":"O campo nome é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get('nome'):
            return JsonResponse({"error":"O campo nome é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        try: 
            data = Categoria.objects.filter(pk=id).get()
            Categoria.objects.filter(pk=id).update(nome=request.data.get('nome'), slug=slugify(request.data.get('nome')))
            return JsonResponse({"estado":"ok", "mensagem":"Categoria modificada com sucesso"}, status=HTTPStatus.OK)
        except Categoria.DoesNotExist:
            raise Http404("Categoria nao encontrada")

    def delete(self, request, id):
        try:
            data = Categoria.objects.get(pk=id)
        except Categoria.DoesNotExist:
            raise Http404("Categoria nao encontrada")

        if Receita.objects.filter(categoria_id=id).exists():
            return JsonResponse({"error":"Erro inesperado"}, status=HTTPStatus.BAD_REQUEST)

        Categoria.objects.get(pk=id)
        data.delete()
        return JsonResponse({"estado":"ok", "mensagem":"Categoria eliminada com sucesso"}, status=HTTPStatus.OK)