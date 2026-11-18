from rest_framework.views import APIView
from django.http import HttpResponse

# Create your views here.

class Class_Exemplo(APIView):
    
    def get(self, request):
        return HttpResponse('Método GET')

    def post(self, request):
        return HttpResponse('Método POST')

class Class_ExemploParametros(APIView):
    
    def get(self, request, id):
        return HttpResponse(f'Método GET - ID: {id}')

    def put(self, request, id):
        return HttpResponse(f'Método PUT - ID: {id}')

    def delete(self, request, id):
        return HttpResponse(f'Método DELETE - ID: {id}')