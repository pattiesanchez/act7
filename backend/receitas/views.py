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
from datetime import datetime
from django.core.files.storage import FileSystemStorage

load_dotenv()

# Create your views here.
class Classe1(APIView):
    
    def get(self, request):
        data = Receita.objects.order_by('-id').all()
        data_json = ReceitaSerializer(data, many=True)
        return JsonResponse(data_json.data, safe=False, status=HTTPStatus.OK)

    def post(self, request):
        if request.data.get('nome')==None or not request.data['nome']:
            return JsonResponse({"error": "O campo nome é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('categoria_id')==None or not request.data['categoria_id']:
            return JsonResponse({"error": "O campo categoria_id é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('tempo')==None or not request.data['tempo']:
            return JsonResponse({"error": "O campo tempo é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('descricao')==None or not request.data['descricao']:
            return JsonResponse({"error": "O campo descricao é obrigatório"}, status=HTTPStatus.BAD_REQUEST)

        #validacao do categoria_id 
        try: 
            categoria = Categoria.objects.get(pk=request.data['categoria_id'])
        except Categoria.DoesNotExist:
            return JsonResponse({"error": "Categoria nao encontrada"}, status=HTTPStatus.BAD_REQUEST)

        # condicao para verificar se ja existe esse nome no banco de dados 
        if Receita.objects.filter(nome=request.data.get('nome')).exists():
            return JsonResponse({"error": "Ja existe uma receita com esse nome"}, status=HTTPStatus.BAD_REQUEST)

        fs = FileSystemStorage()
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return JsonResponse({"error": "Insira uma foto no campo file"}, status=HTTPStatus.BAD_REQUEST)

        try: 
            fs.save(f"receitas/{foto}", request.FILES['foto'])
            fs.url(request.FILES['foto'])
        except Exception as e:
            return JsonResponse({"error": "Erro ao inserir a foto"}, status=HTTPStatus.BAD_REQUEST)

        try:
            Receita.objects.create(
                categoria_id=(request.data.get('categoria_id')),
                nome=(request.data.get('nome')),
                tempo=(request.data.get('tempo')),
                foto=foto,
                descricao=(request.data['descricao']),
                fecha=datetime.now()
            )
            return JsonResponse({"message": "Receita criada com sucesso!"}, status=HTTPStatus.CREATED)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)


class Classe2(APIView):
    
    def get(self, request, id):
        try:
            data = Receita.objects.get(id=id)
            return JsonResponse({"data":{"id": data.id, "nome": data.nome, "slug": data.slug, "tempo": data.tempo, "descricao": data.descricao, "fecha": DateFormat(data.fecha).format("d/m/Y H:i:s"), "categoria_id": data.categoria_id, "categoria": data.categoria.nome, "imagem":f"{os.getenv('BASE_URL')}/uploads/receitas/{data.foto}"}}, status=HTTPStatus.OK)
        except Receita.DoesNotExist:
            raise Http404("Receita nao encontrada")
    
    def post(self, request, id):
        fs = FileSystemStorage()
        fecha = datetime.now()
        foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['foto']))[1]}"
        fs.save(f"exemplo/{foto}", request.FILES['foto'])
        fs.url(request.FILES['foto'])
        return JsonResponse({"estado":"ok", "mensagem":f"Arquivo '{request.FILES['foto'].name}' enviado com sucesso!"}, status=HTTPStatus.CREATED)
