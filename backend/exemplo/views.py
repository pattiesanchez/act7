from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.response import Response
from http import HTTPStatus
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime

# Create your views here.

class Class_Exemplo(APIView):
    
    def get(self, request):
        # return HttpResponse(f'Método GET | id={request.GET.get("id", None)} | slug={request.GET.get("slug", None)}')
        # return Response({"estado":"ok", "mensagem":f"Método GET | id={request.GET.get('id', None)} | slug={request.GET.get('slug', None)}"})
        return JsonResponse({"estado":"ok", "mensagem":f"Metodo GET | id={request.GET.get('id', None)} | slug={request.GET.get('slug')}"}, status=HTTPStatus.OK)

    def post(self, request):
        if request.data.get("correio")==None or request.data.get("senha")==None:
            raise Http404("Faltam dados")
        # return HttpResponse('Método POST')
        return JsonResponse({"estado":"ok", "mensagem":f"Metodo POST | correio={request.data.get('correio')} | senha={request.data.get('senha')}"}, status=HTTPStatus.CREATED)

class Class_ExemploParametros(APIView):
    
    def get(self, request, id):
        return HttpResponse(f'Método GET - ID: {id}')

    def put(self, request, id):
        return HttpResponse(f'Método PUT - ID: {id}')

    def delete(self, request, id):
        return HttpResponse(f'Método DELETE - ID: {id}')

class Class_ExemploUpload(APIView):

    def post(self, request):
        fs = FileSystemStorage()
        fecha = datetime.now()
        foto = f"{datetime.timestamp(fecha)}{os.path.splitext(str(request.FILES['file']))[1]}"
        fs.save(f"exemplo/{foto}", request.FILES['file'])
        fs.url(request.FILES['file'])
        return JsonResponse({"estado":"ok", "mensagem":f"Arquivo '{request.FILES['file'].name}' enviado com sucesso!"}, status=HTTPStatus.CREATED)

        # file = request.FILES.get('file')
        # if file:
        #     # Salvar o arquivo em um diretório específico
        #     caminho_arquivo = f'uploads/{file.name}'
        #     with open(caminho_arquivo, 'wb+') as destino:
        #         for chunk in file.chunks():
        #             destino.write(chunk)
        #     return JsonResponse({"estado":"ok", "mensagem":f"Arquivo '{file.name}' enviado com sucesso!"}, status=HTTPStatus.CREATED)
        # else:
        #     return JsonResponse({"estado":"erro", "mensagem":"Nenhum arquivo enviado"}, status=HTTPStatus.BAD_REQUEST)