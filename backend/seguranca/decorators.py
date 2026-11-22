from functools import wraps
from django.http.response import JsonResponse
from http import HTTPStatus
from jose import jwt 
from django.conf import settings 
import time 


def logado():
    def metodo(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            req = args[0]
            if not req.headers.get('Authorization') or req.headers.get('Authorization')==None:
                return JsonResponse({"error": "Usuario nao autorizado"}, status=HTTPStatus.UNAUTHORIZED)

            header = req.headers.get('Authorization').split(" ")

            try: 
                resultado=jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'])

            except Exception as e:
                return JsonResponse({"error": "Usuario nao autorizado"}, status=HTTPStatus.UNAUTHORIZED)
            
            if int(resultado["exp"])>int(time.time()):
                return func(request, *args, **kwargs)
            else: 
                return JsonResponse({"error": "Usuario nao autorizado"}, status=HTTPStatus.UNAUTHORIZED)
        return _decorator
    return metodo 
 