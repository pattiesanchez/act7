from http import HTTPStatus

from rest_framework.test import APITestCase

from .models import Categoria


class CategoriaAPITests(APITestCase):
    def test_cria_categoria_com_slug(self):
        response = self.client.post('/api/v1/categorias', {'nome': 'Bolos Caseiros'}, format='json')

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        categoria = Categoria.objects.get(nome='Bolos Caseiros')
        self.assertEqual(categoria.slug, 'bolos-caseiros')

    def test_rejeita_categoria_sem_nome(self):
        response = self.client.post('/api/v1/categorias', {}, format='json')

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertFalse(Categoria.objects.exists())
