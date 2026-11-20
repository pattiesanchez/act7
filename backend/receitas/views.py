from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from django.utils.text import slugify
from .serializers import *
from .models import *
from django.utils.dateformat import DateFormat
from dotenv import load_dotenv
import os

load_dotenv()

# Create your views here.
class Classe1(APIView):
    
    def get(self, request):
        data = Receita.objects.order_by('-id').all()
        data_json = ReceitaSerializer(data, many=True)
        return JsonResponse(data_json.data, safe=False, status=HTTPStatus.OK)

class Classe2(APIView):
    
    def get(self, request, id):
        try:
            data = Receita.objects.get(id=id)
            return JsonResponse({"data":{"id": data.id, "nome": data.nome, "slug": data.slug, "tempo": data.tempo, "descricao": data.descricao, "fecha": DateFormat(data.fecha).format("d/m/Y H:i:s"), "categoria_id": data.categoria_id, "categoria": data.categoria.nome, "imagem":f"{os.getenv('BASE_URL')}/uploads/receitas/{data.foto}"}}, status=HTTPStatus.OK)
        except Receita.DoesNotExist:
            raise Http404("Receita nao encontrada")