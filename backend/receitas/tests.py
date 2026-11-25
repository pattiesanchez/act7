from http import HTTPStatus

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from categorias.models import Categoria

from .models import Receita


class ReceitaAPITests(APITestCase):
    def test_busca_receita_por_slug(self):
        usuario = get_user_model().objects.create_user(username='confeiteira', first_name='Ana')
        categoria = Categoria.objects.create(nome='Bolos')
        receita = Receita.objects.create(
            user=usuario,
            categoria=categoria,
            nome='Bolo de Chocolate',
            tempo='45 minutos',
            foto='bolo.jpg',
            descricao='Misture os ingredientes e asse.',
        )

        response = self.client.get(f'/api/v1/receitas/slug/{receita.slug}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        dados = response.json()['data']
        self.assertEqual(dados['id'], receita.id)
        self.assertEqual(dados['nome'], receita.nome)
        self.assertEqual(dados['categoria'], categoria.nome)
        self.assertEqual(dados['user'], usuario.first_name)

    def test_rejeita_criacao_de_receita_sem_autenticacao(self):
        response = self.client.post('/api/v1/receitas', {}, format='json')

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        self.assertFalse(Receita.objects.exists())
