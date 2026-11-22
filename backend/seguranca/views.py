from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
import uuid 
import os 
from dotenv import load_dotenv
from utilidades import utilidades 
from django.contrib.auth import authenticate
from jose import jwt
from django.conf import settings 
from datetime import datetime, timedelta 
import time 

# Create your views here.

class Classe1(APIView):
    
    def post(self, request):
        if request.data.get('nome')==None or not request.data.get('nome'):
            return JsonResponse({"error": "O campo nome é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('email')==None or not request.data.get('email'):
            return JsonResponse({"error": "O campo email é obrigatório"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('password')==None or not request.data.get('password'):
            return JsonResponse({"error": "O campo senha é obrigatório"}, status=HTTPStatus.BAD_REQUEST)

        if User.objects.filter(email=request.data['email']).exists():
            return JsonResponse({"error": f"Este email {request.data.get('email')} já existe na base de dados"}, status=HTTPStatus.BAD_REQUEST)

        token = uuid.uuid4()
        url = f"{os.getenv("BASE_URL")}/api/v1/seguranca/verificacao/{token}"

        try: 
            u=User.objects.create_user(username=request.data['email'], password=request.data['password'], email=request.data['email'],
            first_name=request.data['nome'], last_name="", is_active=0)
            UsersMetadata.objects.create(token=token, user_id=u.id)

            html=f"""
                <h3>Verificacao de conta</h3>
                Ola {request.data['nome']}, seu cadastro foi feito com sucesso. Para ativar o usuario clique no link abaixo:<br/>
                <a href="{url}">{url}</a> 
                <br/>
                Cole o link no seu navegador para ativar: 
                <br/> 
                {url}
            """
            utilidades.sendMail(html, "Verificacao", request.data['email'])

        except Exception as e:
            return JsonResponse({"error": "Usuario nao cadastrado"}, status=HTTPStatus.BAD_REQUEST)
        return JsonResponse({"success": "Usuario cadastrado com sucesso"}, status=HTTPStatus.CREATED)

class Classe2(APIView):
    
    def get(self, request, token):
        if token==None or not token:
            return JsonResponse({"error": "Token nao disponivel"}, status=HTTPStatus.BAD_REQUEST)

        

        try: 
            data=UsersMetadata.objects.filter(token=token).filter(user__is_active=0).get()
            UsersMetadata.objects.filter(token=token).update(token="")
            User.objects.filter(id=data.user_id).update(is_active=1)
            return HttpResponseRedirect(os.getenv("BASE_URL_FRONTEND"))

        except UsersMetadata.DoesNotExist:
            raise Http404 

class Classe3(APIView):

    def post(self, request):

        if request.data.get('email')==None or not request.data['email']:
            return JsonResponse({"error": "Email obrigatorio"}, status=HTTPStatus.BAD_REQUEST)
        if request.data.get('password')==None or not request.data['password']:
            return JsonResponse({"error": "Senha obrigatoria"}, status=HTTPStatus.BAD_REQUEST)

        try: 
            user = User.objects.filter(email=request.data['email']).get()

        except User.DoesNotExist:
            return JsonResponse({"error": "Recurso nao disponivel"}, status=HTTPStatus.NOT_FOUND)

        auth = authenticate(request, username=request.data.get('email'), password=request.data.get('password'))

        if auth is not None: 
            data = datetime.now()
            posterior = data + timedelta(days=1)
            data_numerica = int(datetime.timestamp(posterior))
            payload={"id":user.id, "ISS":os.getenv("BASE_URL"), "iat":int(time.time()), "exp":int(data_numerica)}
            
            try: 
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
                return JsonResponse({"id":user.id, "nome":user.first_name, "token":token}) 
            except Exception as e: 
                return JsonResponse({"error": "Ocorreu um erro inesperado"}, status=HTTPStatus.BAD_REQUEST) 
        else:
            return JsonResponse({"error": "Credenciais invalidas"}, status=HTTPStatus.BAD_REQUEST)
