from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from seguranca.decorators import logado
from django.contrib.auth.models import User
from receitas.serializers import * 
from receitas.models import *
from dotenv import load_dotenv
import os
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.utils.dateformat import DateFormat
from categorias.models import *

# Create your views here.

class Classe1(APIView):

    @logado()
    def post(self, request):
        if request.data.get('id')==None or not request.data.get('id'):
            return JsonResponse({"error": "O campo ID é obrigatorio"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            existe=Receita.objects.filter(pk=request.data['id']).get()
            anterior=existe.foto

        except Receita.DoesNotExist:
            return JsonResponse({"error": "Nao existem receitas cadastradas nesta conta de usuario"}, status=HTTPStatus.BAD_REQUEST)
        
        fs = FileSystemStorage()
        try:
            foto = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['foto']))[1]}"
        except Exception as e:
            return JsonResponse({"error": "Insira uma foto no campo file"}, status=HTTPStatus.BAD_REQUEST)

        if request.FILES['foto'].content_type=='image/jpeg' or request.FILES['foto'].content_type=='image/png':
            try: 
                fs.save(f"receitas/{foto}", request.FILES['foto'])
                fs.url(request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"error": "Erro ao inserir a foto"}, status=HTTPStatus.BAD_REQUEST)

            try:
                Receita.objects.filter(id=request.data['id']).update(foto=foto)
                os.remove(f"./uploads/receitas/{anterior}")
                return JsonResponse({"success": "Foto modificada com sucesso"}, status=HTTPStatus.OK)
            except Exception as e:
                return JsonResponse({"error": "Ocorreu um erro inesperado"}, status=HTTPStatus.BAD_REQUEST)

        else:
            return JsonResponse({"error": "A foto deve ser PNG ou JPEG"}, status=HTTPStatus.BAD_REQUEST)

class Classe2(APIView):

    def get(self, request, slug):
        try:
            data = Receita.objects.filter(slug=slug).get()
            return JsonResponse({"data":{"id": data.id, "nome": data.nome, "slug": data.slug, "tempo": data.tempo, 
            "descricao": data.descricao, "data": DateFormat(data.data).format("d/m/Y H:i:s"), "categoria_id": data.categoria_id, 
            "categoria": data.categoria.nome, "imagem":f"{os.getenv('BASE_URL')}/uploads/receitas/{data.foto}",
            "user_id":data.user_id, "user":data.user.first_name}}, status=HTTPStatus.OK)
        except Receita.DoesNotExist:
            raise Http404("A receita nao existe na base de dados")

class Classe3(APIView):

    def get(self, request):
        data = Receita.objects.order_by('?').all()[:3]
        dados_json=ReceitaSerializer(data, many=True)
        return JsonResponse({"data":dados_json.data}, status=HTTPStatus.OK)

class Classe4(APIView):

    @logado()
    def get(self, request, id):
        try: 
            existe = User.objects.filter(pk=id).get()
        except User.DoesNotExist:
            return JsonResponse({"error": "O usuario nao existe"}, status=HTTPStatus.BAD_REQUEST)

        data = Receita.objects.filter(user_id=id).order_by('-id').all()
        dados_json=ReceitaSerializer(data,many=True)
        return JsonResponse({"data":dados_json.data}, status=HTTPStatus.OK)
    
class Classe5(APIView):

    def get(self, request):
        if request.GET.get('categoria_id')==None or not request.GET.get:
            return JsonResponse({"error": "Erro inesperado"}, status=HTTPStatus.BAD_REQUEST)

        try:
            existe = Categoria.objects.filter(id=request.GET.get('categoria_id')).get()
        except Categoria.DoesNotExist:
            return JsonResponse({"error": "A categoria informada nao existe"}, status=HTTPStatus.BAD_REQUEST)

        data = Receita.objects.filter(categoria_id=request.GET.get('categoria_id')).filter(nome__icontains=request.GET.get('search')).order_by('-id').all()
        dados_json=ReceitaSerializer(data, many=True)
        return JsonResponse({"data":dados_json.data}, status=HTTPStatus.OK)
