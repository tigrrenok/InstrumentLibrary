from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from Instruments.models import Instrument


class GetPageTest(TestCase):
    fixtures = ['instruments.json', 'categories.json', 'tags.json', 'specs.json']

    def setUp(self):
        pass

    def test_mainpage(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'Instruments/index.html')


    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_url = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_data_mainpage(self):
        i = Instrument.published_objects.all().select_related('cat')
        path = reverse('home')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['instruments'], i[:3])

    def test_paginate_mainpage(self):
        path = reverse('home')
        page = 2
        paginate_by = 3
        response = self.client.get(path + f'?page={page}')
        i = Instrument.published_objects.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['instruments'], i[(page - 1) * paginate_by: page * paginate_by])

    def test_instrument_post(self):
        i = Instrument.published_objects.get(pk=12)
        path = reverse('instrument', args=[i.slug])
        response = self.client.get(path)
        self.assertEqual(i.content, response.context_data['instrument'].content)

    def tearDown(self):
        pass