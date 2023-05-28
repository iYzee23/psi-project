from django.contrib import admin
from django.urls import path
from .views import *

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
    path('promeniSifru/', promeniSifru, name="promeniSifru"),
    path('promeniInfo/', promeniInfo, name="promeniInfo"),
    path('resetujLozinku/', admResetujLozinku, name="admResetujLozinku"),
    path('banojNalog/', admBanujNalog, name="admBanujNalog"),
    path('pretraga/', pretraga, name="pretraga")
]