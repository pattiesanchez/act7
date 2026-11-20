from rest_framework.views import APIView
from .models import *
from django.http.response import JsonResponse
from rest_framework.response import Response
from .serializers import *

# Create your views here.

class Classe1(APIView):

    def get(self, request):
        data = Categoria.objects.order_by('-id').all()
        dados_json = CategoriaSerializer(data, many=True)
        return Response(dados_json.data)