
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



from django.contrib.auth.models import Group
from django.test import TestCase, Client
from .models import *
from .forms import *
#

def napraviKor(username,tip):
    korisnik = Uloga()
    korisnik.username = username
    korisnik.set_password("Pedja123!")
    korisnik.email = "proba@proba.com"
    korisnik.imeprezime = "Proba Probic"
    korisnik.tip=tip
    korisnik.datumrodjenja= '2001-01-01'
    korisnik.save()
    return korisnik

class LjubicaTest(TestCase):

#REG
    def test_reg_logged(self):
        c=Client();
        korisnik = napraviKor("KorisnikProba", "K")
        c.login(username="KorisnikProba",password="Pedja123!")

        response=c.post("/reg/")
        self.assertRedirects(response, '/')

    def test_reg_notLogged(self):
        c = Client();

        response = c.post("/reg/")
        self.assertTemplateUsed(response, "registration/reg.html")


#REG_KORISNIK
    def test_reg_korisnik(self):
        c=Client()
        g = Group(name="Korisnici")
        g.save()
        response = c.post('/reg/korisnik', data={
            'username': 'uspesnaProba',
            'password1': 'Pedja123!',
            'password2': 'Pedja123!',
            'ime': 'Proba',
            'prezime': 'Uspesna',
            'email': 'uspesnaProba@uspesnaProba.com',
            'datumrodjenja': '2001-01-01'

        })
        success = c.login(username='uspesnaProba', password='Pedja123!')
        self.assertTrue(success)

    def test_reg_korisnik_vecUlogovan(self):
        c=Client()
        g = Group(name="Korisnici")
        g.save()
        korisnik = napraviKor("KorisnikProba", "K")
        c.login(username="KorisnikProba", password="Pedja123!")

        response = c.post('/reg/korisnik', data={
            'username': 'uspesnaProba',
            'password1': 'Pedja123!',
            'password2': 'Pedja123!',
            'ime': 'Proba',
            'prezime': 'Uspesna',
            'email': 'uspesnaProba@uspesnaProba.com',
            'datumrodjenja': '2001-01-01'

        })
        self.assertRedirects(response, '/')

    def test_reg_korisnik_slabaSifra(self):
        c=Client()
        g = Group(name="Korisnici")
        g.save()
        response = c.post('/reg/korisnik', data={
            'username': 'uspesnaProba',
            'password1': 'Pedja',
            'password2': 'Pedja',
            'ime': 'Proba',
            'prezime': 'Uspesna',
            'email': 'uspesnaProba@uspesnaProba.com',
            'datumrodjenja': '2001-01-01'

        })
        success = c.login(username='uspesnaProba', password='Pedja')
        self.assertFalse(success)

    def test_reg_korisnik_dupliUsername(self):
        c=Client()
        g = Group(name="Korisnici")
        g.save()
        korisnik = napraviKor("neuspesnaProba", "K")
        response = c.post('/reg/korisnik', data={
            'username': 'neuspesnaProba',
            'password1': 'Pedja1234!',
            'password2': 'Pedja1234!',
            'ime': 'Proba',
            'prezime': 'Uspesna',
            'email': 'neuspesnaProba@neuspesnaProba.com',
            'datumrodjenja': '2001-01-01'

        })


        success = c.login(username='neuspesnaProba', password='Pedja1234!')
        self.assertFalse(success)

# class RegKorisnikTest(TestCase):

##REG_AUTOR
    def test_reg_autor(self):
        c = Client()
        g = Group(name="Autori")
        g.save()
        response = c.post('/reg/autor', data={
            'username': 'uspesnaProba',
            'password1': 'Pedja123!',
            'password2': 'Pedja123!',
            'ime': 'Proba',
            'prezime': 'Uspesna',
            'email': 'uspesnaProba@uspesnaProba.com',
            'datumrodjenja': '2001-01-01',
            'biografija':'PROBAPROBAPROBA'

        })
        success = c.login(username='uspesnaProba', password='Pedja123!')
        self.assertTrue(success)

    def test_reg_autor_vecUlogovan(self):
        c = Client()
        korisnik = napraviKor("KorisnikProba", "K")
        c.login(username="KorisnikProba", password="Pedja123!")

        response = c.post('/reg/autor', data={
            'username': 'uspesnaProba',
            'password1': 'Pedja123!',
            'password2': 'Pedja123!',
            'ime': 'Proba',
            'prezime': 'Uspesna',
            'email': 'uspesnaProba@uspesnaProba.com',
            'datumrodjenja': '2001-01-01',
            'biografija':'PROBAPROBAPROBA'

        })

        self.assertRedirects(response, '/')

    def test_reg_autor_slabaSifra(self):
        c = Client()
        g = Group(name="Autori")
        g.save()
        response = c.post('/reg/autor', data={
            'username': 'uspesnaProba',
            'password1': 'Pedja',
            'password2': 'Pedja',
            'ime': 'Proba',
            'prezime': 'Uspesna',
            'email': 'uspesnaProba@uspesnaProba.com',
            'datumrodjenja': '2001-01-01',
            'biografija':'PROBAPROBAPROBA'

        })
        success = c.login(username='uspesnaProba', password='Pedja')
        self.assertFalse(success)

    def test_reg_autor_dupliUsername(self):
        c=Client()
        g = Group(name="Autori")
        g.save()
        korisnik = napraviKor("neuspesnaProba", "A")
        response = c.post('/reg/autor', data={
            'username': 'neuspesnaProba',
            'password1': 'Pedja1234!',
            'password2': 'Pedja1234!',
            'ime': 'Proba',
            'prezime': 'Uspesna',
            'email': 'neuspesnaProba@neuspesnaProba.com',
            'datumrodjenja': '2001-01-01'

        })


        success = c.login(username='neuspesnaProba', password='Pedja1234!')
        self.assertFalse(success)

# class RegIzdKucaTest(TestCase):
#REG_IZDAVACKA_KUCA
    def test_reg_izdKuca(self):
        c = Client()
        g = Group(name="Kuce")
        g.save()
        response = c.post('/reg/kuca', data={
            'username': 'uspesnaProba',
            'password1': 'Pedja123!',
            'password2': 'Pedja123!',
            'naziv': 'Proba',
            'email': 'uspesnaProba@uspesnaProba.com',
            'istorija': 'ISTORIJA',
            'adresa':'Adresa'

        })
        success = c.login(username='uspesnaProba', password='Pedja123!')
        self.assertTrue(success)

    def test_reg_izdKuca_vecUlogovan(self):
        c = Client()
        g = Group(name="Kuce")
        g.save()
        korisnik = napraviKor("KorisnikProba", "K")
        c.login(username="KorisnikProba", password="Pedja123!")

        response = c.post('/reg/kuca', data={
            'username': 'uspesnaProba',
            'password1': 'Pedja123!',
            'password2': 'Pedja123!',
            'naziv': 'Proba',
            'email': 'uspesnaProba@uspesnaProba.com',
            'istorija': 'ISTORIJA',
            'adresa':'Adresa'

        })
        self.assertRedirects(response, '/')

    def test_reg_izdKuca_slabaSifra(self):
        c = Client()
        g = Group(name="Kuce")
        g.save()
        response = c.post('/reg/kuca', data={
            'username': 'uspesnaProba',
            'password1': 'Pedja',
            'password2': 'Pedja',
            'naziv': 'Proba',
            'email': 'uspesnaProba@uspesnaProba.com',
            'istorija': 'ISTORIJA',
            'adresa':'Adresa'

        })
        success = c.login(username='uspesnaProba', password='Pedja')
        self.assertFalse(success)


    def test_reg_izdKuca_dupliUsername(self):
        c=Client()
        g = Group(name="Kuce")
        g.save()
        korisnik = napraviKor("neuspesnaProba", "I")
        response = c.post('/reg/kuca', data={
            'username': 'neuspesnaProba',
            'password1': 'Pedja1234!',
            'password2': 'Pedja1234!',
            'ime': 'Proba',
            'prezime': 'Uspesna',
            'email': 'neuspesnaProba@neuspesnaProba.com',
            'datumrodjenja': '2001-01-01'

        })


        success = c.login(username='neuspesnaProba', password='Pedja1234!')
        self.assertFalse(success)



# class LoginTest(TestCase):
#LOGIN
    def test_login_succ(self):
        c = Client()
        korisnik = napraviKor("KorProba","K")
        c.login(username="KorProba", password="Pedja123!")
        response = c.post('/login/')
        self.assertRedirects(response, '/')

    def test_login_losa_sifra(self):
        c = Client()
        korisnik = napraviKor("KorProba", "K")

        c.login(username="KorProba", password="Pedja123")
        response = c.post('/login/')
        self.assertTemplateUsed(response,"registration/login.html")


    def test_login_los_username(self):
        c = Client()
        korisnik = napraviKor("KorProba", "K")
        c.login(username="PedjaProba", password="Pedja123")
        response = c.post('/login/')
        self.assertTemplateUsed(response, "registration/login.html")


# class LogoutTest(TestCase):
#LOGOUT
    def test_logout(self):

        korisnik = napraviKor('KorProba', 'K')
        self.client.login(username='KorProba', password='Pedja123!')
        self.client.get('/logout/')

        # self.client.logout()

        response = self.client.get('/mojProfil/')

        self.assertEqual(response.status_code, 302)

#PROMENI_SIFRU
    # def test_promeni_sifru_succ(self):
    #     c=Client();
    #     korisnik = napraviKor("KorProba", "K")
    #     c.login(username="KorProba", password="Pedja123!")
    #     response = c.post('/promeniSifru/', data={
    #         'password1': 'Pedja1234!',
    #         'password2': 'Pedja1234!'
    #     })
    #     self.assertRedirects(response,'/profil/')

    def test_promeni_sifru_nejednakeSifre(self):
        c=Client();
        korisnik = napraviKor("KorProba", "K")
        c.login(username="KorProba", password="Pedja123!")
        response = c.post('/promeniSifru/', data={
            'password1': 'Pedja1234!',
            'password2': 'Pedja1234'
        })
        self.assertTemplateUsed(response,"entities/promenaLozinke.html")

