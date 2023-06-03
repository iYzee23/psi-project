from django.contrib import admin
from django.urls import path
from .views import *

'''
Autori: 
- Predrag Pešić 0023/2020
- Aleksa Mićanović 0282/2020
- Luka Nevajda 0370/2020
- Ljubica Muravljov 0071/2020
'''

urlpatterns = [
    path('', index, name="home"),
    path('reg/', reg, name="reg"),
    path('reg/korisnik', regKorisnik, name="regKorisnik"),
    path('reg/autor', regAutor, name="regAutor"),
    path('reg/kuca', regKuca, name="regKuca"),
    path('login/', login_req, name="login"),
    path('logout/', logout_req, name="logout"),
    path('knjiga/<str:knjiga_id>', knjiga, name="knjiga"),
    path('profil/<str:profil_id>', profil, name="profil"),
    path('generisiMesec', generisiMesec, name="generisiMesec"),
    path('profil/', mojProfil, name="mojProfil"),
    path('mojProfil/', mojProfil, name="mojProfil"),
    path('dodajObjavu/', dodajObjavu, name="dodajObjavu"),
    path('izmeniObjavu/', izmeniObjavu, name="izmeniObjavu"),
    path('obrisiObjavu/', obrisiObjavu, name="obrisiObjavu"),
    path('dodajKnjigu/', dodajKnjigu, name="dodajKnjigu"),
    path('izmeniKnjigu/', promeniInfoKnjige, name="izmeniKnjigu"),
    path('promeniSifru/', promeniSifru, name="promeniSifru"),
    path('promeniInfo/', promeniInfo, name="promeniInfo"),
    path('resetujLozinku/', admResetujLozinku, name="admResetujLozinku"),
    path('banojNalog/', admBanujNalog, name="admBanujNalog"),
    path('pretraga/', pretraga, name="pretraga"),
    path('zaprati', zaprati, name="zaprati"),
    path('otprati', otprati, name="otprati"),
    path('licitacije/', licitacije, name="licitacije"),
    path('pretragaAjax/', pretragaAjax, name="pretragaAjax"),
    path('dodajLicitaciju/', dodajLicitaciju, name="dodajLicitaciju")
]