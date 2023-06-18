from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from .models import *
from .views import *
import os


# class PretragaAutoriTest(TestCase):
#     def setUp(self):
#         self.user = Uloga.objects.create_user(username='testuser', password='testpassword', email='test@email.com')
#
#         self.autor1 = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', email='pera@email.com',
#                                            datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
#         self.autor2 = Autor.objects.create(imeprezime='Zivojin Zivojinovic', username='zika', email='zika@email.com',
#                                            datumrodjenja='2001-02-02', biografija='Dolor sit amet', tip='A')
#
#     def test_pretraga_autori_ime(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'Petar'
#
#         response = pretragaAutori(request)
#
#         self.assertEqual(response.status_code, 200)
#
#         self.assertJSONEqual(response.content, ['Petar Petrovic - @pera'])
#
#     def test_pretraga_autori_alias(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'pera'
#
#         response = pretragaAutori(request)
#
#         self.assertEqual(response.status_code, 200)
#
#         self.assertJSONEqual(response.content, ['Petar Petrovic - @pera'])


# class PretragaAjaxTest(TestCase):
#     def setUp(self):
#
#         self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
#                                             prosecnaocena=3.8, email='pera@email.com',
#                                            datumrodjenja='2000-01-01')
#         self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
#                                                  prosecnaocena=3.9, email='mare@email.com',
#                                            datumrodjenja='2001-02-02')
#
#         self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
#                                                              is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum", adresa="Dolor sit amet", tip="I")
#         self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
#                                                       is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum", adresa="Dolor sit amet", tip="I")
#
#         self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
#                                            prosecnaocena=4.7, email='mesa@email.com',
#                                            datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
#         self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
#                                             prosecnaocena=4.8, email='pera@email.com',
#                                             datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
#         self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5, idizdkuca_id='laguna')
#         self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4, idizdkuca_id='kreativnicentar')
#
#     def test_pretraga_ajax_knjige_asc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'i'
#         request.GET['tip'] = 'Knjiga'
#         request.GET['znak']= 'Ocena rastuće'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Prokleta avlija - @234567898765', 'Dervis i smrt - @123456789876']
#         self.assertJSONEqual(response.content, ocekivani_response)
#     def test_pretraga_ajax_knjige_desc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'i'
#         request.GET['tip'] = 'Knjiga'
#         request.GET['znak'] = 'Ocena opadajuće'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Dervis i smrt - @123456789876', 'Prokleta avlija - @234567898765' ]
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_knjige_empty(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'x'
#         request.GET['tip'] = 'Knjiga'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = []
#         self.assertJSONEqual(response.content, ocekivani_response)
#     def test_pretraga_ajax_korisnici_asc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'ic'
#         request.GET['tip'] = 'Korisnik'
#         request.GET['znak'] = 'Ocena rastuće'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Petar Petrovic - @pera','Marko Markovic - @mare']
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_korisnici_desc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'ic'
#         request.GET['tip'] = 'Korisnik'
#         request.GET['znak'] = 'Ocena opadajuće'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Marko Markovic - @mare','Petar Petrovic - @pera']
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_korisnici_empty(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'x'
#         request.GET['tip'] = 'Korisnik'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = []
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_izd_kuce_asc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'a'
#         request.GET['tip'] = 'Kuća'
#         request.GET['znak'] = 'Ocena rastuće'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Kreativni centar - @kreativnicentar', 'Laguna - @laguna']
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_izd_kuce_desc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'a'
#         request.GET['tip'] = 'Kuća'
#         request.GET['znak'] = 'Ocena opadajuće'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Laguna - @laguna', 'Kreativni centar - @kreativnicentar']
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_izd_kuce_empty(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'x'
#         request.GET['tip'] = 'Kuća'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = []
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_autori_asc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'ic'
#         request.GET['tip'] = 'Autor'
#         request.GET['znak'] = 'Ocena rastuće'
#
#         response = pretragaAjax(request)
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Mesa Selimovic - @mesa', 'Ivo Andric - @andric']
#         self.assertJSONEqual(response.content, ocekivani_response)
#     def test_pretraga_ajax_autori_desc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'ic'
#         request.GET['tip'] = 'Autor'
#         request.GET['znak'] = 'Ocena opadajuće'
#
#         response = pretragaAjax(request)
#
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Ivo Andric - @andric', 'Mesa Selimovic - @mesa']
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_autori_empty(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'x'
#         request.GET['tip'] = 'Autor'
#
#         response = pretragaAjax(request)
#
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = []
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_sve_asc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'a'
#         request.GET['tip'] = 'Sve'
#         request.GET['znak'] = 'Ocena rastuće'
#
#         response = pretragaAjax(request)
#
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Prokleta avlija - @234567898765', 'Petar Petrovic - @pera','Marko Markovic - @mare',
#                               'Kreativni centar - @kreativnicentar', 'Laguna - @laguna', 'Mesa Selimovic - @mesa', 'Ivo Andric - @andric']
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_sve_desc(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'a'
#         request.GET['tip'] = 'Sve'
#         request.GET['znak'] = 'Ocena opadajuće'
#
#         response = pretragaAjax(request)
#
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = ['Prokleta avlija - @234567898765', 'Marko Markovic - @mare','Petar Petrovic - @pera',
#                               'Laguna - @laguna', 'Kreativni centar - @kreativnicentar', 'Ivo Andric - @andric', 'Mesa Selimovic - @mesa']
#         self.assertJSONEqual(response.content, ocekivani_response)
#
#     def test_pretraga_ajax_sve_empty(self):
#         request = HttpRequest()
#         request.GET['naziv'] = 'x'
#         request.GET['tip'] = 'Sve'
#
#         response = pretragaAjax(request)
#
#         self.assertEqual(response.status_code, 200)
#         ocekivani_response = []
#         self.assertJSONEqual(response.content, ocekivani_response)


# class ISBNTest(TestCase):
#     def test_ISBN(self):
#         # cuvamo staru vrednost isbna, na kraju testa ce biti bekapovana
#         with open('static/ISBN.txt', 'r') as file:
#             old_isbn=file.read().strip()
#             file.close()
#
#         #testiranje procitajISBN()
#         with open('static/ISBN.txt', 'w') as file:
#             file.write('1234567890123')
#             file.close()
#
#         isbn = procitajISBN()
#
#         self.assertEqual(isbn, '1234567890123')
#
#         #testiranje upisiISBN()
#         upisiISBN('9876543210987')
#         with open('static/ISBN.txt', 'r') as file:
#             isbn = file.read().strip()
#             file.close()
#         self.assertEqual(isbn, '9876543210987')
#
#         #testiranje generisiISBN()
#         with open('static/ISBN.txt', 'w') as file:
#             file.write('1234567890123')
#             file.close()
#
#         isbn = generisiISBN()
#         with open('static/ISBN.txt', 'r') as file:
#             new_isbn = file.read().strip()
#             file.close()
#
#         self.assertEqual(isbn, '1234567890124')
#         self.assertEqual(new_isbn, '1234567890124')
#
#         #bekapovanje starog isbna
#         with open('static/ISBN.txt', 'w') as file:
#             file.write(old_isbn)
#             file.close()


