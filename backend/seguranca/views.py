from rest_framework.views import APIView
from django.http.response import JsonResponse
from http import HTTPStatus
from django.http import Http404
from .models import *

# Create your views here.

class Classe1(APIView):
    
    def post(self, request):
        pass