from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_inicio(request):
    return HttpResponse("Bem-vindo ao sistema ACT 7")