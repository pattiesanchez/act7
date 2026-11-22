from rest_framework.views import APIView
from .models import *
from django.http.response import JsonResponse
from http import HTTPStatus
from django.utils import timezone
#chamada do modulo utilidades
from utilidades import utilidades 
#swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Classe1(APIView): 

    @swagger_auto_schema(
        operation_descripcion="Endpoint para Contato",
        responses={
            200:'Success',
            400:'Bad Request'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nome':openapi.Schema(type=openapi.TYPE_STRING, description='Nome'),
                'email':openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                'telefone':openapi.Schema(type=openapi.TYPE_STRING, description='Telefone'),
                'mensagem':openapi.Schema(type=openapi.TYPE_STRING, description='Mensagem'),
            },
            required=['nome', 'email']
        )
    )

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
            Contato.objects.create(
                nome=request.data["nome"],
                email=request.data["email"],
                telefone=request.data["telefone"],
                mensagem=request.data["mensagem"],
                data=timezone.now()
            )
        except Exception:
            logger.exception("Falha ao salvar contato")

            return JsonResponse(
                {"error": "Erro ao salvar o contato"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

        try:
            from django.utils.html import format_html

            html = format_html(
                """
                <h1>Você tem uma nova mensagem da web</h1>
                <ul>
                    <li>Nome: {}</li>
                    <li>Email: {}</li>
                    <li>Telefone: {}</li>
                    <li>Mensagem: {}</li>
                </ul>
                """,
                request.data["nome"],
                request.data["email"],
                request.data["telefone"],
                request.data["mensagem"]
            )

            utilidades.sendMail(
                html,
                "Nova mensagem do site",
                request.data["email"]
            )
        except Exception:
            logger.exception("Contato salvo, mas houve falha no envio do email")

            return JsonResponse(
                {
                    "success": "Registro criado com sucesso",
                    "aviso": "Falha ao enviar o email"
                },
                status=HTTPStatus.CREATED
            )

        return JsonResponse(
            {"success": "Registro criado e email enviado com sucesso"},
            status=HTTPStatus.CREATED
        )