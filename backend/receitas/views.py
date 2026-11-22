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
from seguranca.decorators import logado
from jose import jwt
from django.conf import settings

# Create your views here.
class Classe1(APIView):
    
    def get(self, request):
        data = Receita.objects.order_by('-id').all()
        data_json = ReceitaSerializer(data, many=True)
        return JsonResponse(data_json.data, safe=False, status=HTTPStatus.OK)

    @logado()
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

        if request.FILES['foto'].content_type=='image/jpeg' or request.FILES['foto'].content_type=='image/png':
            try: 
                fs.save(f"receitas/{foto}", request.FILES['foto'])
                fs.url(request.FILES['foto'])
            except Exception as e:
                return JsonResponse({"error": "Erro ao inserir a foto"}, status=HTTPStatus.BAD_REQUEST)

            header = request.headers.get('Authorization').split(" ")
            resultado=jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'])

            try:
                Receita.objects.create(
                    categoria_id=(request.data.get('categoria_id')),
                    nome=(request.data.get('nome')),
                    tempo=(request.data.get('tempo')),
                    foto=foto,
                    descricao=(request.data['descricao']),
                    data=datetime.now(),
                    user_id=resultado['id']
                )
                return JsonResponse({"message": "Receita criada com sucesso!"}, status=HTTPStatus.CREATED)
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=HTTPStatus.BAD_REQUEST)
        return JsonResponse({"error": "Formato de imagem invalido. Apenas JPEG e PNG sao aceitos"}, status=HTTPStatus.BAD_REQUEST)

class Classe2(APIView):
    
    def get(self, request, id):
        try:
            data = Receita.objects.get(id=id)
            return JsonResponse({"data":{"id": data.id, "nome": data.nome, "slug": data.slug, "tempo": data.tempo, "descricao": data.descricao, 
            "data": DateFormat(data.data).format("d/m/Y H:i:s"), "categoria_id": data.categoria_id, "categoria": data.categoria.nome, 
            "imagem":f"{os.getenv('BASE_URL')}/uploads/receitas/{data.foto}", "user_id":data.user_id, "user":data.user.first_name}}, status=HTTPStatus.OK)
        except Receita.DoesNotExist:
            raise Http404("Receita nao encontrada")

    @logado()
    def post(self, request, id):
        fs = FileSystemStorage()
        data = datetime.now()
        foto = f"{datetime.timestamp(data)}{os.path.splitext(str(request.FILES['foto']))[1]}"
        fs.save(f"exemplo/{foto}", request.FILES['foto'])
        fs.url(request.FILES['foto'])
        return JsonResponse({"estado":"ok", "mensagem":f"Arquivo '{request.FILES['foto'].name}' enviado com sucesso!"}, status=HTTPStatus.CREATED)

    def put(self, request, id):

        try: 
            data = Receita.objects.get(id=id)
        except Receita.DoesNotExist:
            raise Http404("Receita nao encontrada")

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

        try:
            Receita.objects.filter(pk=id).update(
                categoria_id=(request.data.get('categoria_id')),
                slug=slugify(request.data.get('nome')),
                nome=(request.data.get('nome')),
                tempo=(request.data.get('tempo')),
                descricao=(request.data.get('descricao'))
            )
            return JsonResponse({"success": "Receita atualizada com sucesso"}, status=HTTPStatus.OK)
        except Exception as e:
            return JsonResponse({"error": "Erro ao atualizar a receita"}, status=HTTPStatus.BAD_REQUEST)
    
    @logado()
    def delete(self, request, id):
        try: 
            data = Receita.objects.get(id=id)
        except Receita.DoesNotExist:
            raise Http404("Receita nao encontrada")

        #remover os anexos da pasta de uploads do sistema 
        os.remove(f"./uploads/receitas/{data.foto}")
        
        try:
            data.delete()
            return JsonResponse({"success": "Receita deletada com sucesso"}, status=HTTPStatus.OK)
        except Exception as e:
            return JsonResponse({"error": "Erro ao deletar a receita"}, status=HTTPStatus.BAD_REQUEST)