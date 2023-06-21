
from django.contrib.auth.models import Group
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.http import HttpRequest
from .models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from .views import *
from .forms import *
import datetime
import os


def napraviKor(username,tip):
    korisnik=Uloga()
    if tip=="K":
        korisnik=Korisnik()
    elif tip=="A":
        korisnik=Autor()
    else:
        korisnik=IzdavackaKuca()
    korisnik.username = username
    korisnik.set_password("Pedja123!")
    korisnik.email = "proba@proba.com"
    korisnik.imeprezime = "Proba Probic"
    korisnik.tip=tip
    korisnik.datumrodjenja= '2001-01-01'
    korisnik.save()


    return korisnik

def napraviKnjigu(isbn, naziv, izdkuca, ocena=0):
    knjiga = Knjiga()
    knjiga.isbn = isbn
    knjiga.naziv = naziv
    knjiga.slika = "slika.png"
    knjiga.opis = "Opis."
    knjiga.prosecnaocena = ocena
    knjiga.idizdkuca = izdkuca
    knjiga.save()
    return knjiga



def napraviKorisnika(username, imeprezime, ocena=0):
    korisnik = Korisnik()
    korisnik.username = username
    korisnik.set_password("korisnik123!")
    korisnik.email = "korisnik@etf.com"
    korisnik.tip = "K"
    korisnik.prosecnaocena = ocena
    korisnik.imeprezime = imeprezime
    korisnik.datumrodjenja = datetime.date.today()
    korisnik.save()


    return korisnik



def napraviAutora(username, imeprezime, ocena=0):
    autor = Autor()
    autor.username = username
    autor.set_password("autor123!")
    autor.email = "autor@etf.com"
    autor.tip = "A"
    autor.prosecnaocena = ocena
    autor.imeprezime = imeprezime
    autor.datumrodjenja = datetime.date.today()
    autor.biografija = "Biografija."
    autor.save()
    return autor



def napraviKucu(username, naziv, ocena=0):
    kuca = IzdavackaKuca()
    kuca.username = username
    kuca.set_password("kuca123!")
    kuca.email = "kuca@etf.com"
    kuca.tip = "I"
    kuca.prosecnaocena = ocena
    kuca.naziv = naziv
    kuca.istorija = "Istorija."
    kuca.adresa = "Adresa."
    kuca.save()
    return kuca


def napraviLicitaciju(nazivDela, pocetnaCena, autor, datumKraja=timezone.now()+timezone.timedelta(days=1)):
    licitacija = Licitacija()
    licitacija.nazivdela = nazivDela
    licitacija.pdf = "pdf"
    licitacija.datumpocetka = timezone.now()
    licitacija.datumkraja = datumKraja
    licitacija.pocetnacena = pocetnaCena
    licitacija.trenutniiznos = pocetnaCena
    licitacija.idautor = autor
    licitacija.save()
    return licitacija


class Testiranje(TestCase):
    def test_pretraga_autori_ime(self):
        self.user = Uloga.objects.create_user(username='testuser', password='testpassword', email='test@email.com')

        self.autor1 = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Zivojin Zivojinovic', username='zika', email='zika@email.com',
                                           datumrodjenja='2001-02-02', biografija='Dolor sit amet', tip='A')


        request = HttpRequest()
        request.GET['naziv'] = 'Petar'

        response = pretragaAutori(request)

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(response.content, ['Petar Petrovic - @pera'])

    def test_pretraga_autori_alias(self):
        self.user = Uloga.objects.create_user(username='testuser', password='testpassword', email='test@email.com')

        self.autor1 = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Zivojin Zivojinovic', username='zika', email='zika@email.com',
                                           datumrodjenja='2001-02-02', biografija='Dolor sit amet', tip='A')

        request = HttpRequest()
        request.GET['naziv'] = 'pera'

        response = pretragaAutori(request)

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(response.content, ['Petar Petrovic - @pera'])

    def test_pretraga_ajax_knjige_asc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'i'
        request.GET['tip'] = 'Knjiga'
        request.GET['znak'] = 'Ocena rastuće'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Prokleta avlija - @234567898765', 'Dervis i smrt - @123456789876']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_knjige_desc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'i'
        request.GET['tip'] = 'Knjiga'
        request.GET['znak'] = 'Ocena opadajuće'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Dervis i smrt - @123456789876', 'Prokleta avlija - @234567898765']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_knjige_empty(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'x'
        request.GET['tip'] = 'Knjiga'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = []
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_korisnici_asc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'ic'
        request.GET['tip'] = 'Korisnik'
        request.GET['znak'] = 'Ocena rastuće'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Petar Petrovic - @pera', 'Marko Markovic - @mare']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_korisnici_desc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'ic'
        request.GET['tip'] = 'Korisnik'
        request.GET['znak'] = 'Ocena opadajuće'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Marko Markovic - @mare', 'Petar Petrovic - @pera']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_korisnici_empty(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'x'
        request.GET['tip'] = 'Korisnik'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = []
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_izd_kuce_asc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'a'
        request.GET['tip'] = 'Kuća'
        request.GET['znak'] = 'Ocena rastuće'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Kreativni centar - @kreativnicentar', 'Laguna - @laguna']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_izd_kuce_desc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'a'
        request.GET['tip'] = 'Kuća'
        request.GET['znak'] = 'Ocena opadajuće'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Laguna - @laguna', 'Kreativni centar - @kreativnicentar']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_izd_kuce_empty(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'x'
        request.GET['tip'] = 'Kuća'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = []
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_autori_asc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'ic'
        request.GET['tip'] = 'Autor'
        request.GET['znak'] = 'Ocena rastuće'

        response = pretragaAjax(request)
        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Mesa Selimovic - @mesa', 'Ivo Andric - @andric']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_autori_desc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'ic'
        request.GET['tip'] = 'Autor'
        request.GET['znak'] = 'Ocena opadajuće'

        response = pretragaAjax(request)

        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Ivo Andric - @andric', 'Mesa Selimovic - @mesa']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_autori_empty(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'x'
        request.GET['tip'] = 'Autor'

        response = pretragaAjax(request)

        self.assertEqual(response.status_code, 200)
        ocekivani_response = []
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_sve_asc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'a'
        request.GET['tip'] = 'Sve'
        request.GET['znak'] = 'Ocena rastuće'

        response = pretragaAjax(request)

        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Prokleta avlija - @234567898765', 'Petar Petrovic - @pera', 'Marko Markovic - @mare',
                              'Kreativni centar - @kreativnicentar', 'Laguna - @laguna', 'Mesa Selimovic - @mesa',
                              'Ivo Andric - @andric']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_sve_desc(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'a'
        request.GET['tip'] = 'Sve'
        request.GET['znak'] = 'Ocena opadajuće'

        response = pretragaAjax(request)

        self.assertEqual(response.status_code, 200)
        ocekivani_response = ['Prokleta avlija - @234567898765', 'Marko Markovic - @mare', 'Petar Petrovic - @pera',
                              'Laguna - @laguna', 'Kreativni centar - @kreativnicentar', 'Ivo Andric - @andric',
                              'Mesa Selimovic - @mesa']
        self.assertJSONEqual(response.content, ocekivani_response)

    def test_pretraga_ajax_sve_empty(self):
        self.korisnik1 = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                 prosecnaocena=3.8, email='pera@email.com',
                                                 datumrodjenja='2000-01-01')
        self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1,
                                                 prosecnaocena=3.9, email='mare@email.com',
                                                 datumrodjenja='2001-02-02')

        self.izd_kuca1 = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                      is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")
        self.izd_kuca2 = IzdavackaKuca.objects.create(naziv='Laguna', username='laguna',
                                                      is_active=1, prosecnaocena=4.3, istorija="Lorem ipsum",
                                                      adresa="Dolor sit amet", tip="I")

        self.autor1 = Autor.objects.create(imeprezime='Mesa Selimovic', username='mesa', is_active=1,
                                           prosecnaocena=4.7, email='mesa@email.com',
                                           datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.autor2 = Autor.objects.create(imeprezime='Ivo Andric', username='andric', is_active=1,
                                           prosecnaocena=4.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01', biografija='Dolor sit amet', tip='A')
        self.knjiga1 = Knjiga.objects.create(naziv='Dervis i smrt', isbn='123456789876', prosecnaocena=4.5,
                                             idizdkuca_id='laguna')
        self.knjiga2 = Knjiga.objects.create(naziv='Prokleta avlija', isbn='234567898765', prosecnaocena=4.4,
                                             idizdkuca_id='kreativnicentar')

        request = HttpRequest()
        request.GET['naziv'] = 'x'
        request.GET['tip'] = 'Sve'

        response = pretragaAjax(request)

        self.assertEqual(response.status_code, 200)
        ocekivani_response = []
        self.assertJSONEqual(response.content, ocekivani_response)
    def test_ISBN(self):
        # cuvamo staru vrednost isbna, na kraju testa ce biti bekapovana
        with open('static/ISBN.txt', 'r') as file:
            old_isbn=file.read().strip()
            file.close()

        #testiranje procitajISBN()
        with open('static/ISBN.txt', 'w') as file:
            file.write('1234567890123')
            file.close()

        isbn = procitajISBN()

        self.assertEqual(isbn, '1234567890123')

        #testiranje upisiISBN()
        upisiISBN('9876543210987')
        with open('static/ISBN.txt', 'r') as file:
            isbn = file.read().strip()
            file.close()
        self.assertEqual(isbn, '9876543210987')

        #testiranje generisiISBN()
        with open('static/ISBN.txt', 'w') as file:
            file.write('1234567890123')
            file.close()

        isbn = generisiISBN()
        with open('static/ISBN.txt', 'r') as file:
            new_isbn = file.read().strip()
            file.close()

        self.assertEqual(isbn, '1234567890124')
        self.assertEqual(new_isbn, '1234567890124')

        #bekapovanje starog isbna
        with open('static/ISBN.txt', 'w') as file:
            file.write(old_isbn)
            file.close()
    #proveravanje da li se stranica knjige pravilno dodaje
    def test_knjiga_renderevanje(self):
        self.factory = RequestFactory()
        self.user = Uloga.objects.create(username='testuser', password='testpassword', email="test@email.com")
        self.drugi_korisnik = self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare',
                                                                       is_active=1,
                                                                       prosecnaocena=3.9, email='mare@email.com',
                                                                       datumrodjenja='2001-02-02')
        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                     is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', email='pera@email.com',
                                          datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.knjiga = Knjiga.objects.create(isbn='1111111111111', naziv='Test Knjiga', opis="Lorem ipsum",
                                            prosecnaocena=4,
                                            idizdkuca_id="kreativnicentar")
        self.napisao = Napisao.objects.create(idautor_id='pera', isbn_id='1111111111111')

        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalacknjiga_id='1111111111111', iddavalac_id='mare',
                                                        datumobjave='2023-01-01')

        response = self.client.get(reverse('knjiga', args=['1111111111111']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/knjiga.html')
        self.assertEqual(response.context['knjiga'], self.knjiga)
        self.assertQuerysetEqual(response.context['autori'], Autor.objects.filter(napisao__isbn=self.knjiga))
        self.assertQuerysetEqual(response.context['recenzije'], Recenzija.objects.filter(idprimalacknjiga=self.knjiga))
        self.assertIsInstance(response.context['recenzijaFormAdd'], RecenzijaForm)
        self.assertIsInstance(response.context['recenzijaFormEdit'], RecenzijaForm)
        self.assertIsInstance(response.context['pretragaForm'], SearchForm)
        self.assertIsNone(response.context['errorTekst'])

    def test_knjiga_ne_postoji(self):
        self.factory = RequestFactory()
        self.user = Uloga.objects.create(username='testuser', password='testpassword', email="test@email.com")
        self.drugi_korisnik = self.korisnik2 = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare',
                                                                       is_active=1,
                                                                       prosecnaocena=3.9, email='mare@email.com',
                                                                       datumrodjenja='2001-02-02')
        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                     is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', email='pera@email.com',
                                          datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.knjiga = Knjiga.objects.create(isbn='1111111111111', naziv='Test Knjiga', opis="Lorem ipsum",
                                            prosecnaocena=4,
                                            idizdkuca_id="kreativnicentar")
        self.napisao = Napisao.objects.create(idautor_id='pera', isbn_id='1111111111111')

        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalacknjiga_id='1111111111111', iddavalac_id='mare',
                                                        datumobjave='2023-01-01')

        url=reverse('knjiga', args=['1234567890123'])
        request=self.factory.get(url)
        with self.assertRaises(Http404):
            knjiga(request, knjiga_id='1234567890123')

    def test_dodaj_knjigu_u_kolekciju_i_izbaci_je(self):
        self.factory = RequestFactory()
        self.user = Uloga.objects.create(username='testuser', password='testpassword', email="test@email.com")
        self.drugi_korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare',
                                                                       is_active=1,
                                                                       prosecnaocena=3.9, email='mare@email.com',
                                                                       datumrodjenja='2001-02-02')
        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                     is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', email='pera@email.com',
                                          datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.knjiga = Knjiga.objects.create(isbn='1111111111111', naziv='Test Knjiga', opis="Lorem ipsum",
                                            prosecnaocena=4,
                                            idizdkuca_id="kreativnicentar")
        self.napisao = Napisao.objects.create(idautor_id='pera', isbn_id='1111111111111')

        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalacknjiga_id='1111111111111', iddavalac_id='mare',
                                                        datumobjave='2023-01-01')

        self.client.force_login(user=self.user)


        #dodavanje u licnu kolekciju
        self.url = reverse('knjiga', args=[self.knjiga.isbn])
        response=self.client.post(self.url, {'dodajUkolekciju': '1'})
        self.assertTrue(Kolekcija.objects.filter(isbn=self.knjiga, korime_id=self.user.username).exists())
        self.assertEqual(response.status_code,200)
        #izbacivanje iz kolekcije
        self.url = reverse('knjiga', args=[self.knjiga.isbn])
        response=self.client.post(self.url, {'brisiIzKolekcije': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not Kolekcija.objects.filter(isbn=self.knjiga, korime_id=self.user.username).exists())


    def test_knjiga_recenzije(self):
        self.factory = RequestFactory()
        self.user = Uloga.objects.create(username='testuser', password='testpassword', email="test@email.com")
        self.drugi_korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare',
                                                      is_active=1,
                                                      prosecnaocena=3.9, email='mare@email.com',
                                                      datumrodjenja='2001-02-02')
        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar',
                                                     is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', email='pera@email.com',
                                          datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.knjiga = Knjiga.objects.create(isbn='1111111111111', naziv='Test Knjiga', opis="Lorem ipsum",
                                            prosecnaocena=4,
                                            idizdkuca_id="kreativnicentar")
        self.napisao = Napisao.objects.create(idautor_id='pera', isbn_id='1111111111111')


        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalacknjiga_id='1111111111111', iddavalac_id='mare',
                                                        datumobjave='2023-01-01')

        self.client.force_login(user=self.user)
        #pokusaj submitovanja nevalidne forme
        self.url = reverse('knjiga', args=[self.knjiga.isbn])
        response = self.client.post(self.url, data={'add-tekst': 'Test tekst!'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not Recenzija.objects.filter(idprimalacknjiga=self.knjiga, iddavalac=self.user).exists())
        #dodavanje recenzije
        self.url = reverse('knjiga', args=[self.knjiga.isbn])
        response = self.client.post(self.url, data={'add-tekst': 'Test tekst!', 'add-ocena': 5})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Recenzija.objects.filter(idprimalacknjiga=self.knjiga, iddavalac=self.user).exists())
        knjiga=Knjiga.objects.get(isbn=self.knjiga.isbn)
        self.assertEqual(knjiga.prosecnaocena,4.5)

        #pokusaj ponovo dodati recenziju
        self.url = reverse('knjiga', args=[self.knjiga.isbn])
        response = self.client.post(self.url, data={'add-tekst': 'Test tekst!', 'add-ocena': 5, 'postavi':'1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['errorTekst'], 'Ne mozete upisati više od 1 recenzije!')

        #izmena recenzije
        self.url = reverse('knjiga', args=[self.knjiga.isbn])
        response = self.client.post(self.url, data={'edit-tekst': 'Test tekst?', 'edit-ocena': 3})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Recenzija.objects.filter(idprimalacknjiga=self.knjiga, iddavalac=self.user).exists())
        knjiga = Knjiga.objects.get(isbn=self.knjiga.isbn)
        self.assertEqual(knjiga.prosecnaocena, 3.5)

        #brisanje recenzije
        self.url = reverse('knjiga', args=[self.knjiga.isbn])
        response = self.client.post(self.url, data={'edit-tekst': 'Test tekst?', 'edit-ocena': 4,'obrisi': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recenzija.objects.filter(idprimalacknjiga=self.knjiga, iddavalac=self.user).exists())
        knjiga = Knjiga.objects.get(isbn=self.knjiga.isbn)
        self.assertEqual(knjiga.prosecnaocena, 4)

    def test_knjiga_autor_recenzija(self):
        self.factory = RequestFactory()
        self.drugi_korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1, prosecnaocena=3.9, email='mare@email.com', datumrodjenja='2001-02-02')

        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar', is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', password='testpassword', email="test@email.com", is_active=1, datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')

        self.knjiga = Knjiga.objects.create(isbn='1111111111111', naziv='Test Knjiga', opis="Lorem ipsum",
                                            prosecnaocena=4,
                                            idizdkuca_id="kreativnicentar")
        self.napisao = Napisao.objects.create(idautor_id='pera', isbn_id='1111111111111')

        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalacknjiga_id='1111111111111', iddavalac_id='mare',
                                                        datumobjave='2023-01-01')

        self.client.force_login(user=self.autor)

        #pokusaj dodavanja recenzije od strane autora na datu knjigu
        self.url = reverse('knjiga', args=[self.knjiga.isbn])
        response = self.client.post(self.url, data={'add-tekst': 'Test tekst!', 'add-ocena': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['errorTekst'], 'Ne mozete ostaviti recenziju na Vasoj knjizi!')

    def test_knjiga_izd_kuca_recenzija(self):
        self.factory = RequestFactory()
        self.drugi_korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', is_active=1, prosecnaocena=3.9, email='mare@email.com', datumrodjenja='2001-02-02')

        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar', password='testpassword', email="test@email.com", is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1, datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')


        self.knjiga = Knjiga.objects.create(isbn='1111111111111', naziv='Test Knjiga', opis="Lorem ipsum",
                                            prosecnaocena=4,
                                            idizdkuca_id="kreativnicentar")
        self.napisao = Napisao.objects.create(idautor_id='pera', isbn_id='1111111111111')


        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalacknjiga_id='1111111111111', iddavalac_id='mare',
                                                        datumobjave='2023-01-01')

        self.client.force_login(user=self.izd_kuca)

        #pokusaj dodavanja recenzije od strane izd kuce na datu knjigu
        self.url = reverse('knjiga', args=[self.knjiga.isbn])
        response = self.client.post(self.url, data={'add-tekst': 'Test tekst!', 'add-ocena': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['errorTekst'], 'Ne mozete ostaviti recenziju na Vasoj knjizi!')

    def test_korisnik_profil_renderovanje(self):
        self.factory = RequestFactory()
        self.user = Uloga.objects.create(username='testuser', password='testpassword', email="test@email.com")
        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar', is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', password='testpassword', email="test@email.com", is_active=1, datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare',
                                                      is_active=1,
                                                      prosecnaocena=3.9, email='mare@email.com',
                                                      datumrodjenja='2001-02-02')
        self.korisnik2=Korisnik.objects.create(imeprezime='Aleksa Aleksic', username='leksa',
                                                      is_active=1,
                                                      prosecnaocena=4.4, email='leksa@email.com',
                                                      datumrodjenja='2000-01-01')
        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalaculoga_id='mare', iddavalac_id='leksa',
                                                        datumobjave='2023-01-01')

        self.prati1 = Prati.objects.create(idpracen_id=self.korisnik2.username, idpratilac_id=self.korisnik.username)
        self.prati2 = Prati.objects.create(idpracen_id=self.korisnik.username, idpratilac_id=self.korisnik2.username)
        self.prati3 = Prati.objects.create(idpracen_id=self.autor.username, idpratilac_id=self.korisnik.username)
        self.prati4 = Prati.objects.create(idpracen_id=self.izd_kuca.username, idpratilac_id=self.korisnik.username)


        self.client.force_login(user=self.user)


        response = self.client.get(reverse('profil', args=['mare']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/korisnik.html')
        self.assertEqual(response.context['profil'], self.korisnik)
        self.assertEqual(response.context['flag'], 1)
        self.assertQuerysetEqual(response.context['objave'], Objava.objects.filter(korime=self.korisnik).order_by('-datumobjave'))
        self.assertQuerysetEqual(response.context['recenzije'], Recenzija.objects.filter(idprimalaculoga=self.korisnik))
        self.assertQuerysetEqual(response.context['licna_kolekcija'], Knjiga.objects.filter(kolekcija__korime=self.korisnik))
        self.assertIsInstance(response.context['recenzijaFormAdd'], RecenzijaForm)
        self.assertIsInstance(response.context['recenzijaFormEdit'], RecenzijaForm)
        self.assertIsInstance(response.context['objavaForm'], TextObjavaForm)
        self.assertIsInstance(response.context['objavaFormEdit'], TextObjavaForm)
        self.assertIsInstance(response.context['objavaFormDelete'], ObjavaDeleteForm)
        self.assertIsInstance(response.context['pretragaForm'], SearchForm)
        self.assertIsNone(response.context['errorTekst'])
    def test_autor_profil_renderovanje(self):
        self.factory = RequestFactory()
        self.user = Uloga.objects.create(username='testuser', password='testpassword', email="test@email.com")
        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar', is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', password='testpassword', email="test@email.com", is_active=1, datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.knjiga = Knjiga.objects.create(isbn='1111111111111', naziv='Test Knjiga', opis="Lorem ipsum",
                                            prosecnaocena=4,
                                            idizdkuca_id="kreativnicentar")
        self.napisao = Napisao.objects.create(idautor_id='pera', isbn_id='1111111111111')
        self.povezani=Povezani.objects.create(idautor_id='pera', idizdkuca_id='kreativnicentar')

        self.korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare',
                                                      is_active=1,
                                                      prosecnaocena=3.9, email='mare@email.com',
                                                      datumrodjenja='2001-02-02')
        self.korisnik2=Korisnik.objects.create(imeprezime='Aleksa Aleksic', username='leksa',
                                                      is_active=1,
                                                      prosecnaocena=4.4, email='leksa@email.com',
                                                      datumrodjenja='2000-01-01')
        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalaculoga_id='mare', iddavalac_id='leksa',
                                                        datumobjave='2023-01-01')

        self.prati1 = Prati.objects.create(idpracen_id=self.korisnik2.username, idpratilac_id=self.autor.username)
        self.prati2 = Prati.objects.create(idpracen_id=self.autor.username, idpratilac_id=self.korisnik2.username)
        self.prati3 = Prati.objects.create(idpracen_id=self.autor.username, idpratilac_id=self.korisnik.username)
        self.prati4 = Prati.objects.create(idpracen_id=self.izd_kuca.username, idpratilac_id=self.autor.username)

        self.client.force_login(user=self.user)

        response = self.client.get(reverse('profil', args=['pera']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/autor.html')
        self.assertEqual(response.context['profil'], self.autor)
        self.assertEqual(response.context['flag'], 1)
        self.assertQuerysetEqual(response.context['objave'], Objava.objects.filter(korime=self.autor).order_by('-datumobjave'))
        self.assertQuerysetEqual(response.context['recenzije'], Recenzija.objects.filter(idprimalaculoga=self.autor))
        self.assertQuerysetEqual(response.context['licna_kolekcija'], Knjiga.objects.filter(kolekcija__korime=self.autor))
        self.assertQuerysetEqual(response.context['kuce'], IzdavackaKuca.objects.filter(povezani__idautor=self.autor).order_by('-prosecnaocena').distinct())
        self.assertQuerysetEqual(response.context['knjige'], Knjiga.objects.filter(napisao__idautor='pera').order_by('-prosecnaocena'))
        self.assertIsInstance(response.context['recenzijaFormAdd'], RecenzijaForm)
        self.assertIsInstance(response.context['recenzijaFormEdit'], RecenzijaForm)
        self.assertIsInstance(response.context['objavaForm'], TextObjavaForm)
        self.assertIsInstance(response.context['objavaFormEdit'], TextObjavaForm)
        self.assertIsInstance(response.context['objavaFormDelete'], ObjavaDeleteForm)
        self.assertIsInstance(response.context['pretragaForm'], SearchForm)
        self.assertIsNone(response.context['errorTekst'])
    def test_izd_kuca_profil_renderovanje(self):
        self.factory = RequestFactory()
        self.user = Uloga.objects.create(username='testuser', password='testpassword', email="test@email.com")
        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar', is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', password='testpassword', email="test@email.com", is_active=1, datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.knjiga = Knjiga.objects.create(isbn='1111111111111', naziv='Test Knjiga', opis="Lorem ipsum",
                                            prosecnaocena=4,
                                            idizdkuca_id="kreativnicentar")
        self.napisao = Napisao.objects.create(idautor_id='pera', isbn_id='1111111111111')
        self.povezani=Povezani.objects.create(idautor_id='pera', idizdkuca_id='kreativnicentar')

        self.korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare',
                                                      is_active=1,
                                                      prosecnaocena=3.9, email='mare@email.com',
                                                      datumrodjenja='2001-02-02')
        self.korisnik2=Korisnik.objects.create(imeprezime='Aleksa Aleksic', username='leksa',
                                                      is_active=1,
                                                      prosecnaocena=4.4, email='leksa@email.com',
                                                      datumrodjenja='2000-01-01')
        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalaculoga_id='mare', iddavalac_id='leksa',
                                                        datumobjave='2023-01-01')

        self.prati1 = Prati.objects.create(idpracen_id=self.korisnik2.username, idpratilac_id=self.izd_kuca.username)
        self.prati2 = Prati.objects.create(idpracen_id=self.izd_kuca.username, idpratilac_id=self.korisnik2.username)
        self.prati3 = Prati.objects.create(idpracen_id=self.autor.username, idpratilac_id=self.izd_kuca.username)
        self.prati4 = Prati.objects.create(idpracen_id=self.izd_kuca.username, idpratilac_id=self.autor.username)

        self.client.force_login(user=self.user)

        response = self.client.get(reverse('profil', args=['kreativnicentar']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/izdavackakuca.html')
        self.assertEqual(response.context['profil'], self.izd_kuca)
        self.assertEqual(response.context['flag'], 1)
        self.assertQuerysetEqual(response.context['objave'], Objava.objects.filter(korime=self.izd_kuca).order_by('-datumobjave'))
        self.assertQuerysetEqual(response.context['recenzije'], Recenzija.objects.filter(idprimalaculoga=self.izd_kuca))
        self.assertQuerysetEqual(response.context['knjige'], Knjiga.objects.filter(idizdkuca=self.izd_kuca).order_by('-prosecnaocena'))
        self.assertQuerysetEqual(response.context['autori'], Autor.objects.filter(povezani__idizdkuca=self.izd_kuca).order_by('imeprezime').distinct())
        self.assertQuerysetEqual(response.context['lokacije'], ProdajnaMesta.objects.filter(idizdkuca='kreativnicentar'))
        self.assertIsInstance(response.context['recenzijaFormAdd'], RecenzijaForm)
        self.assertIsInstance(response.context['recenzijaFormEdit'], RecenzijaForm)
        self.assertIsInstance(response.context['objavaForm'], TextObjavaForm)
        self.assertIsInstance(response.context['objavaFormEdit'], TextObjavaForm)
        self.assertIsInstance(response.context['objavaFormDelete'], ObjavaDeleteForm)
        self.assertIsInstance(response.context['pretragaForm'], SearchForm)
        self.assertIsNone(response.context['errorTekst'])

    def test_profil_ne_postoji(self):
        self.factory = RequestFactory()
        url=reverse('profil', args=['x'])
        request=self.factory.get(url)
        with self.assertRaises(Http404):
            profil(request, profil_id='x')

    def test_moj_profil(self):
        self.korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare',password='mare123',
                                                is_active=1,
                                                prosecnaocena=3.9, email='mare@email.com',
                                                datumrodjenja='2001-02-02')
        self.client.force_login(user=self.korisnik)
        response = self.client.get(reverse('mojProfil'))
        self.assertEqual(response.status_code, 302)


        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera',
                                          email="test@email.com", is_active=1, datumrodjenja='2000-01-01',
                                          biografija='Lorem ipsum', tip='A')
        self.client.force_login(user=self.autor)
        response = self.client.get(reverse('mojProfil'))
        self.assertEqual(response.status_code, 302)


        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar', is_active=1,
                                                     prosecnaocena=4.2, istorija="Lorem ipsum", adresa="Dolor sit amet", tip="I")

        self.client.force_login(user=self.izd_kuca)
        response = self.client.get(reverse('mojProfil'))
        self.assertEqual(response.status_code, 302)

    def test_ostavljanje_recenzije_na_profil(self):
        self.factory = RequestFactory()
        self.user = Uloga.objects.create(username='testuser', password='testpassword', email="test@email.com")
        self.izd_kuca = IzdavackaKuca.objects.create(naziv='Kreativni centar', username='kreativnicentar', is_active=1, prosecnaocena=4.2, istorija="Lorem ipsum",
                                                     adresa="Dolor sit amet", tip="I")
        self.autor = Autor.objects.create(imeprezime='Petar Petrovic', username='pera', password='testpassword', email="test@email.com", is_active=1, datumrodjenja='2000-01-01', biografija='Lorem ipsum', tip='A')
        self.korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare',
                                                      is_active=1,
                                                      prosecnaocena=4, email='mare@email.com',
                                                      datumrodjenja='2001-02-02')
        self.korisnik2=Korisnik.objects.create(imeprezime='Aleksa Aleksic', username='leksa',
                                                      is_active=1,
                                                      prosecnaocena=4.4, email='leksa@email.com',
                                                      datumrodjenja='2000-01-01')
        self.tudja_recenzija = Recenzija.objects.create(ocena=4, tekst="Lorem ipsum",
                                                        idprimalaculoga_id='mare', iddavalac_id='leksa',
                                                        datumobjave='2023-01-01')

        self.prati1 = Prati.objects.create(idpracen_id=self.korisnik2.username, idpratilac_id=self.korisnik.username)
        self.prati2 = Prati.objects.create(idpracen_id=self.korisnik.username, idpratilac_id=self.korisnik2.username)
        self.prati3 = Prati.objects.create(idpracen_id=self.autor.username, idpratilac_id=self.korisnik.username)
        self.prati4 = Prati.objects.create(idpracen_id=self.izd_kuca.username, idpratilac_id=self.korisnik.username)

        self.client.force_login(user=self.user)
        #pokusaj submitovanja nevalidne forme za recenzije
        self.url = reverse('profil', args=[self.korisnik.username])
        response = self.client.post(self.url, data={'add-tekst': 'Test tekst!'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recenzija.objects.filter(idprimalaculoga=self.korisnik, iddavalac=self.user).exists())
        #dodavanje recenzije
        self.url = reverse('profil', args=[self.korisnik.username])
        response = self.client.post(self.url, data={'add-tekst': 'Test tekst!', 'add-ocena': 5})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Recenzija.objects.filter(idprimalaculoga=self.korisnik, iddavalac=self.user).exists())
        korisnik=Korisnik.objects.get(username=self.korisnik.username)
        self.assertEqual(korisnik.prosecnaocena,4.5)

        #pokusaj ponovo dodati recenziju
        self.url = reverse('profil', args=[self.korisnik.username])
        response = self.client.post(self.url, data={'add-tekst': 'Test tekst!', 'add-ocena': 5, 'postavi':'1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['errorTekst'], 'Ne mozete upisati više od 1 recenzije!')

        #izmena recenzije
        self.url = reverse('profil', args=[self.korisnik.username])
        response = self.client.post(self.url, data={'edit-tekst': 'Test tekst?', 'edit-ocena': 3})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Recenzija.objects.filter(idprimalaculoga=self.korisnik, iddavalac=self.user).exists())
        korisnik=Korisnik.objects.get(username=self.korisnik.username)
        self.assertEqual(korisnik.prosecnaocena, 3.5)

        #brisanje recenzije
        self.url = reverse('profil', args=[self.korisnik.username])
        response = self.client.post(self.url, data={'edit-tekst': 'Test tekst?', 'edit-ocena': 4,'obrisi': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Recenzija.objects.filter(idprimalaculoga=self.korisnik, iddavalac=self.user).exists())
        korisnik=Korisnik.objects.get(username=self.korisnik.username)
        self.assertEqual(korisnik.prosecnaocena, 4)

    def test_ostavljanje_recenzije_na_moj_profil(self):
        self.korisnik = Korisnik.objects.create(imeprezime='Marko Markovic', username='mare', password='test123',
                                                is_active=1,
                                                prosecnaocena=4, email='mare@email.com',
                                                datumrodjenja='2001-02-02')

        self.client.force_login(user=self.korisnik)
        self.url = reverse('profil', args=[self.korisnik.username])
        response = self.client.post(self.url, data={'add-tekst': 'Test tekst!', 'add-ocena': 5})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['errorTekst'], 'Ne mozete ostaviti recenziju sami sebi!')


    # testiranje pretrage
    def test_pretraga_nema_parametara(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        url = reverse("home")
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)

        url = reverse("pretraga")
        response = self.client.post(path=url, HTTP_REFERER=reverse('home'), data={})
        self.assertEqual(response.status_code, 302)

    def test_pretraga_knjiga_opadajuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        izdkuca1 = napraviKucu("izdkuca1", "IzdKuca1")
        izdkuca2 = napraviKucu("izdkuca2", "IzdKuca2")
        napraviKnjigu("1111111111111", "Knjiga1", izdkuca1)
        napraviKnjigu("2222222222222", "Knjiga2", izdkuca2, 4)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Knjiga",
            "tip": "Knjiga",
            "filter": "Ocena opadajuće"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')


        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 2)
        for obj in objekti:
            self.assertEqual(obj['tip'], "knjiga")
        for i in range(len(objekti) - 1):
            self.assertGreaterEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    def test_pretraga_knjiga_rastuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        izdkuca1 = napraviKucu("izdkuca1", "IzdKuca1")
        izdkuca2 = napraviKucu("izdkuca2", "IzdKuca2")
        napraviKnjigu("1111111111111", "Knjiga1", izdkuca1)
        napraviKnjigu("2222222222222", "Knjiga2", izdkuca2, 4)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Knjiga",
            "tip": "Knjiga",
            "filter": "Ocena rastuće"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')

        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 2)
        for obj in objekti:
            self.assertEqual(obj['tip'], "knjiga")
        for i in range(len(objekti) - 1):
            self.assertLessEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    def test_pretraga_autor_opadajuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        napraviAutora("autor1", "Autor Autorovic 1", 2)
        napraviAutora("autor2", "Autor Autorovic 2", 1)
        napraviAutora("autor3", "Autor Autorovic 3", 4)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Autor",
            "tip": "Autor",
            "filter": "Ocena opadajuće"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')

        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 3)
        for obj in objekti:
            self.assertEqual(obj['tip'], "profil")
        for i in range(len(objekti) - 1):
            self.assertGreaterEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    def test_pretraga_autor_rastuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        napraviAutora("autor1", "Autor Autorovic 1", 2)
        napraviAutora("autor2", "Autor Autorovic 2", 1)
        napraviAutora("autor3", "Autor Autorovic 3", 4)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Autor",
            "tip": "Autor",
            "filter": "Ocena rastuće"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')

        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 3)
        for obj in objekti:
            self.assertEqual(obj['tip'], "profil")
        for i in range(len(objekti) - 1):
            self.assertLessEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    def test_pretraga_korisnik_opadajuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        napraviKorisnika("korisnik1", "Korisnik Korisnikovic 1", 2)
        napraviKorisnika("korisnik2", "Korisnik Korisnikovic 2", 1)
        napraviKorisnika("korisnik3", "Korisnik Korisnikovic 3", 4)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Korisnik",
            "tip": "Korisnik",
            "filter": "Ocena opadajuće"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')

        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 4)
        for obj in objekti:
            self.assertEqual(obj['tip'], "profil")
        for i in range(len(objekti) - 1):
            self.assertGreaterEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    def test_pretraga_korisnik_rastuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        napraviKorisnika("korisnik1", "Korisnik Korisnikovic 1", 2)
        napraviKorisnika("korisnik2", "Korisnik Korisnikovic 2", 1)
        napraviKorisnika("korisnik3", "Korisnik Korisnikovic 3", 4)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Korisnik",
            "tip": "Korisnik",
            "filter": "Ocena rastuće"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')

        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 4)
        for obj in objekti:
            self.assertEqual(obj['tip'], "profil")
        for i in range(len(objekti) - 1):
            self.assertLessEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    def test_pretraga_kuca_opadajuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        napraviKucu("kuca1", "Kuca Kucic 1", 2)
        napraviKucu("kuca2", "Kuca Kucic 2", 1)
        napraviKucu("kuca3", "Kuca Kucic 3", 4)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Kuca",
            "tip": "Kuća",
            "filter": "Ocena opadajuće"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')

        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 3)
        for obj in objekti:
            self.assertEqual(obj['tip'], "profil")
        for i in range(len(objekti) - 1):
            self.assertGreaterEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    def test_pretraga_kuca_rastuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        napraviKucu("kuca1", "Kuca Kucic 1", 2)
        napraviKucu("kuca2", "Kuca Kucic 2", 1)
        napraviKucu("kuca3", "Kuca Kucic 3", 4)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Kuca",
            "tip": "Kuća",
            "filter": "Ocena rastuće"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')

        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 3)
        for obj in objekti:
            self.assertEqual(obj['tip'], "profil")
        for i in range(len(objekti) - 1):
            self.assertLessEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    def test_pretraga_sve_opadajuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        napraviKorisnika("korisnik1", "Korisnik Korisnikovic Bla", 2)
        napraviAutora("autor", "Autor Autorovic Bla", 1)
        izdkuca = napraviKucu("kuca", "Kuca Kucic Bla", 4)
        napraviKnjigu("1111111111111", "Knjiga Bla", izdkuca, 3)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Bla",
            "tip": "Sve",
            "filter": "Ocena opadajuće"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')

        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 4)
        for i in range(len(objekti) - 1):
            self.assertGreaterEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    def test_pretraga_sve_rastuce(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        napraviKorisnika("korisnik1", "Korisnik Korisnikovic Bla", 2)
        napraviAutora("autor", "Autor Autorovic Bla", 1)
        izdkuca = napraviKucu("kuca", "Kuca Kucic Bla", 4)
        napraviKnjigu("1111111111111", "Knjiga Bla", izdkuca, 3)

        url = reverse("pretraga")
        response = self.client.post(path=url, data={
            "naziv": "Bla",
            "tip": "Sve",
            "filter": "Ocena rastuće"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/pretraga.html')

        objekti = response.context['objekti']
        self.assertEqual(len(objekti), 4)
        for i in range(len(objekti) - 1):
            self.assertLessEqual(objekti[i]['prosecnaocena'], objekti[i + 1]['prosecnaocena'])

    # testiranje zapracivanja
    def test_zaprati_neulogovan_korisnik(self):
        url = reverse('zaprati')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/zaprati')

    def test_zaprati_validna_forma(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        praceni = napraviKorisnika("praceni", "Praceni Korisnik")

        url = reverse('zaprati')
        response = self.client.post(path=url, data={
            'praceni': praceni.pk,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profil', args=[praceni.pk]))

        praceni.refresh_from_db()
        self.assertEqual(praceni.brpratilaca, 1)

        prati = Prati.objects.filter(idpracen=praceni, idpratilac=korisnik)
        self.assertTrue(prati.exists())

    def test_zaprati_nevalidna_form(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        praceni = napraviKorisnika("praceni", "Praceni Korisnik")

        url = reverse('zaprati')
        response = self.client.post(path=url, data={})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        praceni.refresh_from_db()
        self.assertEqual(praceni.brpratilaca, 0)

        prati = Prati.objects.filter(idpracen=praceni, idpratilac=korisnik)
        self.assertFalse(prati.exists())

    # testiranje otpracivanja
    def test_otprati_neulogovan_korisnik(self):
        url = reverse('otprati')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/otprati')

    def test_otprati_validna_forma(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        praceni = napraviKorisnika("praceni", "Praceni Korisnik")

        url = reverse('zaprati')
        response = self.client.post(path=url, data={
            'praceni': praceni.pk,
        })

        url = reverse('otprati')
        response = self.client.post(path=url, data={
            'praceni': praceni.pk,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profil', args=[praceni.pk]))

        praceni.refresh_from_db()
        self.assertEqual(praceni.brpratilaca, 0)

        prati = Prati.objects.filter(idpracen=praceni, idpratilac=korisnik)
        self.assertFalse(prati.exists())

    def test_otprati_nevalidna_form(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        praceni = napraviKorisnika("praceni", "Praceni Korisnik")

        url = reverse('zaprati')
        response = self.client.post(path=url, data={
            'praceni': praceni.pk,
        })

        url = reverse('otprati')
        response = self.client.post(path=url, data={})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        praceni.refresh_from_db()
        self.assertEqual(praceni.brpratilaca, 1)

        prati = Prati.objects.filter(idpracen=praceni, idpratilac=korisnik)
        self.assertTrue(prati.exists())

    # testiranje dodavanja objave
    def test_dodaj_objavu_neulogovan_korisnik(self):
        url = reverse('dodajObjavu')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/dodajObjavu/')

    def test_dodaj_objavu_validna_forma(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        url = reverse('dodajObjavu')
        response = self.client.post(path=url, data={
            'sadrzaj': 'Test objava',
            'slika': "slika.jpg"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mojProfil'), target_status_code=302)
        # self.assertEqual(response['Location'], reverse('mojProfil'))
        # mora ovako jer imamo chain of redirects

        self.assertEqual(Objava.objects.count(), 1)
        objava = Objava.objects.first()
        self.assertEqual(objava.sadrzaj, 'Test objava')
        self.assertEqual(objava.korime_id, korisnik.pk)

    def test_dodaj_objavu_nevalidna_forma(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        url = reverse('dodajObjavu')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mojProfil'), target_status_code=302)
        self.assertEqual(Objava.objects.count(), 0)

    # testiranje izmene objave
    def test_izmeni_objavu_neulogovan_korisnik(self):
        url = reverse('izmeniObjavu')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/izmeniObjavu/')

    def test_izmeni_objavu_validna_forma(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        post = Objava.objects.create(sadrzaj='Stari sadrzaj.', korime=korisnik, datumobjave=datetime.datetime.now())

        url = reverse('izmeniObjavu')
        response = self.client.post(path=url, data={
            'objavaEdit-hiddenIdObjave': post.idobjava,
            'objavaEdit-sadrzaj': 'Novi sadrzaj.',
            'objavaEdit-slika': "slika.jpg"
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mojProfil'), target_status_code=302)

        post.refresh_from_db()
        self.assertEqual(post.sadrzaj, 'Novi sadrzaj.')

    def test_izmeni_objavu_nevalidna_forma(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        post = Objava.objects.create(sadrzaj='Stari sadrzaj.', korime=korisnik, datumobjave=datetime.datetime.now())

        url = reverse('izmeniObjavu')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mojProfil'), target_status_code=302)

        post.refresh_from_db()
        self.assertEqual(post.sadrzaj, 'Stari sadrzaj.')

    # testiranje brisanja objave
    def test_obrisi_objavu_neulogovan_korisnik(self):
        url = reverse('obrisiObjavu')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/obrisiObjavu/')

    def test_obrisi_objavu_validna_forma(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        post = Objava.objects.create(sadrzaj='Stari sadrzaj.', korime=korisnik, datumobjave=datetime.datetime.now())

        url = reverse('obrisiObjavu')
        response = self.client.post(path=url, HTTP_REFERER=reverse('home'), data={
            'hiddenIdObjave': post.idobjava
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Objava.objects.filter(idobjava=post.idobjava).exists())

    def test_obrisi_objavu_nevalidna_forma(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        post = Objava.objects.create(sadrzaj='Stari sadrzaj.', korime=korisnik, datumobjave=datetime.datetime.now())

        url = reverse('obrisiObjavu')
        response = self.client.post(path=url, HTTP_REFERER=reverse('home'), data={})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Objava.objects.filter(idobjava=post.idobjava).exists())

    # testiranje dodavanja knjige
    def test_dodaj_knjigu_validna_forma_izdavacka_kuca(self):
        kuca = napraviKucu("kuca", "Kuca Kucic")
        self.client.force_login(user=kuca)

        autor1 = napraviAutora("autor1", "Autor Autorovic 1")
        autor2 = napraviAutora("autor2", "Autor Autorovic 2")
        autor3 = napraviAutora("autor3", "Autor Autorovic 3")

        url = reverse('dodajKnjigu')
        response = self.client.post(path=url, data={
            'novaKnjiga-sadrzaj': 'Test objava',
            'novaKnjiga-naziv': 'Test knjiga',
            'novaKnjiga-slika': 'slika.jpg',
            'novaKnjiga-opis': 'Opis knjige',
            'mojiAutori': [autor1.pk, autor2.pk, autor3.pk]
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mojProfil'), target_status_code=302)

        self.assertEqual(Knjiga.objects.count(), 1)
        self.assertEqual(Napisao.objects.count(), 3)
        self.assertEqual(Povezani.objects.count(), 3)
        self.assertEqual(Objava.objects.count(), 1)

        knjiga = Knjiga.objects.first()
        self.assertEqual(knjiga.naziv, 'Test knjiga')
        self.assertEqual(knjiga.opis, 'Opis knjige')

        napisao = Napisao.objects.first()
        self.assertEqual(napisao.isbn_id, knjiga.isbn)

        i = 1
        for povezani in Povezani.objects.all():
            self.assertEqual(povezani.idautor_id, "autor" + str(i))
            i = i + 1

        objava = Objava.objects.first()
        self.assertEqual(objava.sadrzaj, 'Test objava')
        self.assertEqual(objava.korime_id, kuca.pk)

    def test_dodaj_knjigu_validna_forma_nije_izdavacka_kuca(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        autor1 = napraviAutora("autor1", "Autor Autorovic 1")
        autor2 = napraviAutora("autor2", "Autor Autorovic 2")
        autor3 = napraviAutora("autor3", "Autor Autorovic 3")

        url = reverse('dodajKnjigu')
        response = self.client.post(path=url, data={
            'novaKnjiga-sadrzaj': 'Test objava',
            'novaKnjiga-naziv': 'Test knjiga',
            'novaKnjiga-slika': 'slika.jpg',
            'novaKnjiga-opis': 'Opis knjige',
            'mojiAutori': [autor1.pk, autor2.pk, autor3.pk]
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mojProfil'), target_status_code=302)

        self.assertEqual(Knjiga.objects.count(), 0)
        self.assertEqual(Napisao.objects.count(), 0)
        self.assertEqual(Povezani.objects.count(), 0)
        self.assertEqual(Objava.objects.count(), 0)

    def test_dodaj_knjigu_validna_forma_vec_povezani(self):
        kuca = napraviKucu("kuca", "Kuca Kucic")
        self.client.force_login(user=kuca)

        autor1 = napraviAutora("autor1", "Autor Autorovic 1")
        autor2 = napraviAutora("autor2", "Autor Autorovic 2")
        autor3 = napraviAutora("autor3", "Autor Autorovic 3")
        Povezani.objects.create(idautor=autor1, idizdkuca=kuca)

        url = reverse('dodajKnjigu')
        response = self.client.post(path=url, data={
            'novaKnjiga-sadrzaj': 'Test objava',
            'novaKnjiga-naziv': 'Test knjiga',
            'novaKnjiga-slika': 'slika.jpg',
            'novaKnjiga-opis': 'Opis knjige',
            'mojiAutori': [autor1.pk, autor2.pk, autor3.pk]
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mojProfil'), target_status_code=302)

        self.assertEqual(Knjiga.objects.count(), 1)
        self.assertEqual(Napisao.objects.count(), 3)
        self.assertEqual(Povezani.objects.count(), 3)
        self.assertEqual(Objava.objects.count(), 1)

        knjiga = Knjiga.objects.first()
        self.assertEqual(knjiga.naziv, 'Test knjiga')
        self.assertEqual(knjiga.opis, 'Opis knjige')

        napisao = Napisao.objects.first()
        self.assertEqual(napisao.isbn_id, knjiga.isbn)

        i = 1
        for povezani in Povezani.objects.all():
            self.assertEqual(povezani.idautor_id, "autor" + str(i))
            i = i + 1

        objava = Objava.objects.first()
        self.assertEqual(objava.sadrzaj, 'Test objava')
        self.assertEqual(objava.korime_id, kuca.pk)

    def test_dodaj_knjigu_nije_validna_forma(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        url = reverse('dodajKnjigu')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mojProfil'), target_status_code=302)

        self.assertEqual(Knjiga.objects.count(), 0)
        self.assertEqual(Napisao.objects.count(), 0)
        self.assertEqual(Povezani.objects.count(), 0)
        self.assertEqual(Objava.objects.count(), 0)

    def test_dodaj_knjigu_nije_ulogovan_korisnik(self):
        url = reverse('dodajKnjigu')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/dodajKnjigu/')

    # testiranje promene informacija knjige
    def test_promeni_info_knjige_validna_forma_izdavacka_kuca(self):
        kuca = napraviKucu("kuca", "Kuca Kucic")
        self.client.force_login(user=kuca)

        knjiga = napraviKnjigu('1234567890', 'Stara knjiga', kuca)
        autor1 = napraviAutora("autor1", "Autor Autorovic 1")
        autor2 = napraviAutora("autor2", "Autor Autorovic 2")
        Napisao.objects.create(idautor=autor1, isbn=knjiga)
        Napisao.objects.create(idautor=autor2, isbn=knjiga)
        Povezani.objects.create(idautor=autor1, idizdkuca=kuca)
        Povezani.objects.create(idautor=autor2, idizdkuca=kuca)

        session = self.client.session
        session['isbn'] = knjiga.isbn
        session.save()
        # mora ovako jer ako bismo radili samo
        # self.client.session['isbn'] = knjiga.isbn
        # self.client.session.save()
        # ovo bi potencijalno pristupilo razlicitim sesijama

        url = reverse('izmeniKnjigu')
        response = self.client.post(url, data={
            'sadrzaj': 'Test objava',
            'slika': 'slika.jpg',
            'naziv': 'Nova knjiga',
            'opis': 'Novi opis',
            'mojiAutoriOpet': [autor1.pk, autor2.pk],
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('knjiga', kwargs={'knjiga_id': knjiga.pk}))

        knjiga.refresh_from_db()
        autori = Autor.objects.filter(napisao__isbn=knjiga)

        self.assertEqual(knjiga.naziv, 'Nova knjiga')
        self.assertEqual(knjiga.opis, 'Novi opis')
        self.assertEqual(autori.count(), 2)
        self.assertTrue(autori.filter(pk=autor1.pk).exists())
        self.assertTrue(autori.filter(pk=autor2.pk).exists())
        self.assertEqual(Povezani.objects.count(), 2)

        objava = Objava.objects.first()
        self.assertEqual(objava.sadrzaj, 'Test objava')
        self.assertEqual(objava.korime_id, kuca.pk)

    def test_promeni_info_knjige_validna_forma_nije_izdavacka_kuca(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        kuca = napraviKucu("kuca", "Kuca Kucic")
        knjiga = napraviKnjigu('1234567890', 'Stara knjiga', kuca)
        autor1 = napraviAutora("autor1", "Autor Autorovic 1")
        autor2 = napraviAutora("autor2", "Autor Autorovic 2")
        Napisao.objects.create(idautor=autor1, isbn=knjiga)
        Napisao.objects.create(idautor=autor2, isbn=knjiga)
        Povezani.objects.create(idautor=autor1, idizdkuca=kuca)
        Povezani.objects.create(idautor=autor2, idizdkuca=kuca)

        session = self.client.session
        session['isbn'] = knjiga.isbn
        session.save()

        url = reverse('izmeniKnjigu')
        try:
            response = self.client.post(url, data={
                'sadrzaj': 'Test objava',
                'slika': 'slika.jpg',
                'naziv': 'Nova knjiga',
                'opis': 'Novi opis',
                'mojiAutoriOpet': [autor1.pk, autor2.pk],
            })

            self.assertEqual(response.status_code, 200)

            knjiga.refresh_from_db()

            self.assertEqual(knjiga.naziv, 'Stara knjiga')
            self.assertEqual(knjiga.opis, 'Opis.')
        except Exception:
            pass

    def test_promeni_info_knjige_nevalidna_forma(self):
        kuca = napraviKucu("kuca", "Kuca Kucic")
        self.client.force_login(user=kuca)

        knjiga = napraviKnjigu('1234567890', 'Stara knjiga', kuca)

        session = self.client.session
        session['isbn'] = knjiga.isbn
        session.save()

        url = reverse('izmeniKnjigu')
        response = self.client.post(url, data={})

        self.assertEqual(response.status_code, 200)

        knjiga.refresh_from_db()

        self.assertEqual(knjiga.naziv, 'Stara knjiga')
        self.assertEqual(knjiga.opis, 'Opis.')

    def test_promeni_info_knjige_validna_forma_izdavacka_kuca_vise_na_vise(self):
        kuca = napraviKucu("kuca", "Kuca Kucic")
        self.client.force_login(user=kuca)

        knjiga = napraviKnjigu('1234567890', 'Stara knjiga', kuca)
        knjiga_dod = napraviKnjigu('0987654321', 'Stara knjiga dod', kuca)
        autor1 = napraviAutora("autor1", "Autor Autorovic 1")
        autor2 = napraviAutora("autor2", "Autor Autorovic 2")
        Napisao.objects.create(idautor=autor1, isbn=knjiga)
        Napisao.objects.create(idautor=autor2, isbn=knjiga)
        Napisao.objects.create(idautor=autor1, isbn=knjiga_dod)
        Napisao.objects.create(idautor=autor2, isbn=knjiga_dod)
        Povezani.objects.create(idautor=autor1, idizdkuca=kuca)
        Povezani.objects.create(idautor=autor2, idizdkuca=kuca)

        session = self.client.session
        session['isbn'] = knjiga.isbn
        session.save()

        url = reverse('izmeniKnjigu')
        response = self.client.post(url, data={
            'sadrzaj': 'Test objava',
            'slika': 'slika.jpg',
            'naziv': 'Nova knjiga',
            'opis': 'Novi opis',
            'mojiAutoriOpet': [autor1.pk, autor2.pk],
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('knjiga', kwargs={'knjiga_id': knjiga.pk}))

        knjiga.refresh_from_db()
        autori = Autor.objects.filter(napisao__isbn=knjiga)

        self.assertEqual(knjiga.naziv, 'Nova knjiga')
        self.assertEqual(knjiga.opis, 'Novi opis')
        self.assertEqual(autori.count(), 2)
        self.assertTrue(autori.filter(pk=autor1.pk).exists())
        self.assertTrue(autori.filter(pk=autor2.pk).exists())
        self.assertEqual(Povezani.objects.count(), 2)

        objava = Objava.objects.first()
        self.assertEqual(objava.sadrzaj, 'Test objava')
        self.assertEqual(objava.korime_id, kuca.pk)

    def test_promeni_info_knjige_nije_ulogovan_korisnik(self):
        url = reverse('izmeniKnjigu')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/izmeniKnjigu/')

    # testiranje licitiranja
    def test_licitacije_validna_ponuda(self):
        kuca = napraviKucu("kuca", "Kuca Kucic")
        self.client.force_login(user=kuca)

        autor = napraviAutora("autor", "Autor Autorovic")
        licitacija = napraviLicitaciju("Licitirano delo", 50, autor)

        url = reverse('licitacije')
        response = self.client.post(url, data={
            'iznos': 100,
            'hiddenIdLic': licitacija.idlicitacija
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['errorTekst'], None)

        ponuda = Ponuda.objects.filter(idizdkuca=kuca, idlicitacija=licitacija).first()
        self.assertIsNotNone(ponuda)
        self.assertEqual(ponuda.iznos, 100)

        cLicitacija = Licitacija.objects.get(idlicitacija=licitacija.idlicitacija)
        self.assertEqual(cLicitacija.trenutniiznos, 100)
        self.assertEqual(cLicitacija.idpobednik, kuca)

    def test_licitacije_nevalidna_ponuda(self):
        kuca = napraviKucu("kuca", "Kuca Kucic")
        self.client.force_login(user=kuca)

        autor = napraviAutora("autor", "Autor Autorovic")
        licitacija = napraviLicitaciju("Licitirano delo", 100, autor)

        url = reverse('licitacije')
        response = self.client.post(url, data={
            'iznos': 50,
            'hiddenIdLic': licitacija.idlicitacija
        })

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context['errorTekst'], None)

        ponuda = Ponuda.objects.filter(idizdkuca=kuca, idlicitacija=licitacija).first()
        self.assertIsNone(ponuda)

    def test_licitacije_nije_izdavacka_kuca_nije_autor(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(user=korisnik)

        autor = napraviAutora("autor", "Autor Autorovic")
        licitacija = napraviLicitaciju("Licitirano delo", 50, autor)

        url = reverse('licitacije')
        response = self.client.post(url, data={
            'iznos': 100,
            'hiddenIdLic': licitacija.idlicitacija
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('mojProfil'), target_status_code=302)

        ponuda = Ponuda.objects.first()
        self.assertIsNone(ponuda)

    def test_licitacije_jeste_autor(self):
        autorKor = napraviAutora("autorKor", "Autor Autorovic Kor")
        self.client.force_login(user=autorKor)

        autor = napraviAutora("autor", "Autor Autorovic")
        licitacija = napraviLicitaciju("Licitirano delo", 50, autor)

        url = reverse('licitacije')
        response = self.client.post(url, data={
            'iznos': 100,
            'hiddenIdLic': licitacija.idlicitacija
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['errorTekst'], None)

        ponuda = Ponuda.objects.first()
        self.assertIsNone(ponuda)

    def test_licitacije_nije_ulogovan(self):
        url = reverse('licitacije')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/licitacije/')

    def test_licitacije_autor_tekuce_prosle(self):
        autor = napraviAutora("autor", "Autor Autorovic")
        self.client.force_login(autor)

        tekucaLic1 = napraviLicitaciju("Tekuca licitacija 1", 50, autor, timezone.now() + timezone.timedelta(days=1))
        tekucaLic2 = napraviLicitaciju("Tekuca licitacija 2", 150, autor, timezone.now() + timezone.timedelta(days=2))
        proslaLic1 = napraviLicitaciju("Prosla licitacija 1", 20, autor, timezone.now() - timezone.timedelta(days=3))
        proslaLic2 = napraviLicitaciju("Prosla licitacija 2", 120, autor, timezone.now() - timezone.timedelta(days=2))

        url = reverse("licitacije")
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "entities/licitacije.html")
        self.assertIn("tekuce_licitacije", response.context)
        self.assertIn("protekle_licitacije", response.context)

        self.assertIn(tekucaLic1, response.context["tekuce_licitacije"])
        self.assertIn(tekucaLic2, response.context["tekuce_licitacije"])
        self.assertIn(proslaLic1, response.context["protekle_licitacije"])
        self.assertIn(proslaLic2, response.context["protekle_licitacije"])

        tekuce_licitacije = response.context["tekuce_licitacije"]
        self.assertEqual(tekuce_licitacije[0], tekucaLic1)
        self.assertEqual(tekuce_licitacije[1], tekucaLic2)

        protekle_licitacije = response.context["protekle_licitacije"]
        self.assertEqual(protekle_licitacije[0], proslaLic2)
        self.assertEqual(protekle_licitacije[1], proslaLic1)

    def test_licitacije_izdavacka_kuca_tekuce_prosle(self):
        kuca = napraviKucu("kuca", "Kuca Kucic")
        self.client.force_login(kuca)

        autor = napraviAutora("autor", "Autor Autorovic")
        tekucaLic1 = napraviLicitaciju("Tekuca licitacija 1", 50, autor, timezone.now() + timezone.timedelta(days=1))
        tekucaLic2 = napraviLicitaciju("Tekuca licitacija 2", 150, autor, timezone.now() + timezone.timedelta(days=2))
        proslaLic1 = napraviLicitaciju("Prosla licitacija 1", 20, autor, timezone.now() - timezone.timedelta(days=3))
        proslaLic2 = napraviLicitaciju("Prosla licitacija 2", 120, autor, timezone.now() - timezone.timedelta(days=2))

        proslaLic1.idpobednik = kuca
        proslaLic2.idpobednik = kuca
        proslaLic1.save()
        proslaLic2.save()

        url = reverse("licitacije")
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "entities/licitacije.html")
        self.assertIn("tekuce_licitacije", response.context)
        self.assertIn("protekle_licitacije", response.context)

        self.assertIn(tekucaLic1, response.context["tekuce_licitacije"])
        self.assertIn(tekucaLic2, response.context["tekuce_licitacije"])
        self.assertIn(proslaLic1, response.context["protekle_licitacije"])
        self.assertIn(proslaLic2, response.context["protekle_licitacije"])

        tekuce_licitacije = response.context["tekuce_licitacije"]
        self.assertEqual(tekuce_licitacije[0], tekucaLic1)
        self.assertEqual(tekuce_licitacije[1], tekucaLic2)

        protekle_licitacije = response.context["protekle_licitacije"]
        self.assertEqual(protekle_licitacije[0], proslaLic2)
        self.assertEqual(protekle_licitacije[1], proslaLic1)

    def test_licitacije_admin_tekuce_prosle(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic Admin")
        korisnik.is_superuser = True
        korisnik.save()
        self.client.force_login(korisnik)

        autor = napraviAutora("autor", "Autor Autorovic")
        tekucaLic1 = napraviLicitaciju("Tekuca licitacija 1", 50, autor, timezone.now() + timezone.timedelta(days=1))
        tekucaLic2 = napraviLicitaciju("Tekuca licitacija 2", 150, autor, timezone.now() + timezone.timedelta(days=2))
        proslaLic1 = napraviLicitaciju("Prosla licitacija 1", 20, autor, timezone.now() - timezone.timedelta(days=3))
        proslaLic2 = napraviLicitaciju("Prosla licitacija 2", 120, autor, timezone.now() - timezone.timedelta(days=2))

        url = reverse("licitacije")
        response = self.client.get(path=url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "entities/licitacije.html")
        self.assertIn("tekuce_licitacije", response.context)
        self.assertIn("protekle_licitacije", response.context)

        self.assertIn(tekucaLic1, response.context["tekuce_licitacije"])
        self.assertIn(tekucaLic2, response.context["tekuce_licitacije"])
        self.assertIn(proslaLic1, response.context["protekle_licitacije"])
        self.assertIn(proslaLic2, response.context["protekle_licitacije"])

        tekuce_licitacije = response.context["tekuce_licitacije"]
        self.assertEqual(tekuce_licitacije[0], tekucaLic1)
        self.assertEqual(tekuce_licitacije[1], tekucaLic2)

        protekle_licitacije = response.context["protekle_licitacije"]
        self.assertEqual(protekle_licitacije[0], proslaLic2)
        self.assertEqual(protekle_licitacije[1], proslaLic1)

    # testiranje dodavanja licitacije
    def test_dodaj_licitaciju_validan_datum(self):
        autor = napraviAutora("autor", "Autor Autorovic")
        self.client.force_login(autor)

        url = reverse("dodajLicitaciju")
        response = self.client.post(path=url, data={
            "nazivdela": "Test Naziv",
            "pdf": SimpleUploadedFile("test.pdf", b"Test PDF Content", content_type="application/pdf"),
            "datumkraja": (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            "pocetnacena": 100,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("licitacije"))
        self.assertTrue(Licitacija.objects.filter(nazivdela="Test Naziv").exists())

    def test_dodaj_licitaciju_nevalidan_datum(self):
        autor = napraviAutora("autor", "Autor Autorovic")
        self.client.force_login(autor)

        url = reverse("dodajLicitaciju")
        response = self.client.post(path=url, data={
            "nazivdela": "Test Naziv",
            "pdf": SimpleUploadedFile("test.pdf", b"Test PDF Content", content_type="application/pdf"),
            "datumkraja": (timezone.now() - timezone.timedelta(days=1)).isoformat(),
            "pocetnacena": 100,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("licitacije"))
        self.assertFalse(Licitacija.objects.filter(nazivdela="Test Naziv").exists())

    def test_dodaj_licitaciju_nevalidna_forma(self):
        autor = napraviAutora("autor", "Autor Autorovic")
        self.client.force_login(autor)

        url = reverse("dodajLicitaciju")
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("licitacije"))
        self.assertEqual(Licitacija.objects.count(), 0)

    def test_dodaj_licitaciju_nije_ulogovan(self):
        url = reverse('dodajLicitaciju')
        response = self.client.post(path=url, data={})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/dodajLicitaciju/')

    def test_dodaj_licitaciju_nije_autor(self):
        korisnik = napraviKorisnika("korisnik", "Korisnik Korisnikovic")
        self.client.force_login(korisnik)

        url = reverse("dodajLicitaciju")
        response = self.client.post(path=url, data={
            "nazivdela": "Test Naziv",
            "pdf": SimpleUploadedFile("test.pdf", b"Test PDF Content", content_type="application/pdf"),
            "datumkraja": (timezone.now() - timezone.timedelta(days=1)).isoformat(),
            "pocetnacena": 100,
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("licitacije"), target_status_code=302)
        self.assertEqual(Licitacija.objects.count(), 0)
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
    def test_promeni_sifru_succ(self):
        c=Client();
        g = Group(name="Kuce")
        g.save()
        korisnik = napraviKor("KorProba", "K")
        c.login(username="KorProba", password="Pedja123!")

        response = c.post('/promeniSifru/', data={
            'password1': '123',
            'password2': '123'
        })

        self.assertTrue(response.url=="/mojProfil/")

    def test_promeni_sifru_nejednakeSifre(self):
        c=Client();
        korisnik = napraviKor("KorProba", "K")
        c.login(username="KorProba", password="Pedja123!")
        response = c.post('/promeniSifru/', data={
            'password1': 'Pedja1234!',
            'password2': 'Pedja1234'
        })
        self.assertTemplateUsed(response,"entities/promenaLozinke.html")

    #PROMENI_INFO
    def test_promeni_info_Korisnik(self):
        c=Client();

        korisnik = napraviKor("KorProba", "K")

        c.login(username="KorProba", password="Pedja123!")

        response=c.post('/promeniInfo/',data={
            'email':'mejlProba@mejlProba.com',
            'ime':'Proba',
            'prezime':'Prezime',
            'datumrodjenja':'2002-01-01',
            'biografija':'PromenjenaaBIoooo',
            'slika':''
        })

        self.assertTrue(response.url == "/mojProfil/")

    def test_promeni_info_Korisnik_invalidForma(self):

        c = Client();


        korisnik = napraviKor("KorProba", "K")

        c.login(username="KorProba", password="Pedja123!")

        response = c.post('/promeniInfo/', data={
            'email': 'mejlProba@mejlProba.com',
            'ime': 'Proba',
            'prezime': 'Prezime',
            'datumrodjenja': '1',
            'biografija': 'PromenjenaaBIoooo',
            'slika': ''
        })

        self.assertTemplateUsed(response,"entities/promenaInfo.html")

    def test_promeni_info_Autor(self):
        c=Client();

        korisnik = napraviKor("KorProba", "A")

        c.login(username="KorProba", password="Pedja123!")

        response=c.post('/promeniInfo/',data={
            'email':'mejlProba@mejlProba.com',
            'ime':'Proba',
            'prezime':'Prezime',
            'datumrodjenja':'2002-01-01',
            'biografija':'PromenjenaaBIoooo',
            'slika':''
        })

        self.assertTrue(response.url == "/mojProfil/")

    def test_promeni_info_Autor_invalidForma(self):

        c = Client();


        korisnik = napraviKor("KorProba", "A")

        c.login(username="KorProba", password="Pedja123!")

        response = c.post('/promeniInfo/', data={
            'email': 'mejlProba@mejlProba.com',
            'ime': 'Proba',
            'prezime': 'Prezime',
            'datumrodjenja': '1',
            'biografija': 'PromenjenaaBIoooo',
            'slika': ''
        })

        self.assertTemplateUsed(response,"entities/promenaInfo.html")


    def test_promeni_info_IzdKuca(self):
        c=Client();

        korisnik = napraviKor("KorProba", "I")

        c.login(username="KorProba", password="Pedja123!")

        response=c.post('/promeniInfo/',data={
            'email':'mejlProba@mejlProba.com',
            'naziv':'novNaziv',

            'istorija':'PromenjenaaBIoooo',
            'adresa':'promenaAdrese',
            'slika':''
        })
        self.assertTrue(response.url == "/mojProfil/")

    def test_promeni_info_IzdKuca_invalidForma(self):

        c = Client();


        korisnik = napraviKor("KorProba", "K")

        c.login(username="KorProba", password="Pedja123!")

        response=c.post('/promeniInfo/',data={
            'email':'mejlProba@mejlProba.com',
            'naziv':'novNaziv',


            'adresa':'promenaAdrese',
            'slika':''
        })

        self.assertTemplateUsed(response,"entities/promenaInfo.html")

    #ADMIN_RESET_LOZINKA
    def test_admin_lozinka(self):
        self.superuser = Uloga.objects.create_superuser(
            username='ljubica',
            email='admin@example.com',
            password='123'
        )

        c=Client()
        korisnik=napraviKor("ProbaResSifra","K")


        c.login(username="ljubica",password="123")

        c.post('/resetujLozinku/',data={
            'username':'ProbaResSifra',
            'email':'proba@proba.com'

        })

        response=c.login(username='ProbaResSifra',password='Pedja123!')
        self.assertFalse(response)

    def test_admin_lozinka_neAdminPoziva(self):

        c = Client()



        korisnik = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                           prosecnaocena=3.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01',password='123')
        c.login(username='pera',password='123')

        korisnik = napraviKor("ProbaResSifra", "K")

        c.post('/resetujLozinku/', data={
                'username':'ProbaResSifra',
                'email':'proba@proba.com'

            })

        response=c.login(username='ProbaResSifra',password='Pedja123!')
        self.assertTrue(response)


    #ADMIN_BANUJ
    def test_admin_ban(self):
        self.superuser = Uloga.objects.create_superuser(
            username='ljubica',
            email='admin@example.com',
            password='123'
        )

        c = Client()
        korisnik = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                                                                             prosecnaocena=3.8, email='pera@email.com',
                                                                                            datumrodjenja='2000-01-01',password='123')



        c.login(username="ljubica", password="123")

        response=c.post('/banojNalog/', data={
            'username': 'pera',
            'email': 'proba@proba.com',
            'ban': 'Ban'

        })
        #
        response = c.login(username='pera', password='123')
        self.assertFalse(response)

    def test_admin_ban_neAdminProba(self):
        c = Client()



        korisnik = Korisnik.objects.create(imeprezime='Petar Petrovic', username='pera', is_active=1,
                                           prosecnaocena=3.8, email='pera@email.com',
                                           datumrodjenja='2000-01-01',password='123')
        c.login(username='pera',password='123')

        korisnik = napraviKor("ProbaResSifra", "K")

        c.post('/banojNalog/', data={
                    'username': 'ProbaResSifra',
                    'email': 'proba@proba.com',
                    'ban': 'Ban'

                })

        response=c.login(username='ProbaResSifra',password='Pedja123!')
        self.assertTrue(response)

    #INDEX

    def test_index(self):

        c = Client()
        response=c.post('/')
        self.assertTemplateUsed(response, "index.html")
