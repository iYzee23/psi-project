# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
'''
Autori:
- Predrag Pešić 0023/2020
- Aleksa Mićanović 0282/2020
- Luka Nevajda 0370/2020
- Ljubica Muravljov 0071/2020
'''

class Uloga(AbstractUser):
    id = None
    last_login = None
    first_name = None
    last_name = None
    # is_active = None
    # is_staff = None
    # is_superuser = None
    date_joined = None
    username = models.CharField(db_column='KorIme', primary_key=True, max_length=20, validators=[UnicodeUsernameValidator()])
    password = models.CharField(db_column='Sifra', max_length=128)
    email = models.CharField(db_column='Email', max_length=40)
    slika = models.ImageField(db_column='Slika', null=True, upload_to='ulogaImgs/', default="ulogaImgs/default.jpg")
    brpratilaca = models.IntegerField(db_column='BrPratilaca', default=0)
    prosecnaocena = models.DecimalField(db_column='ProsecnaOcena', max_digits=5, decimal_places=2, default=0)
    tip = models.CharField(db_column='Tip', max_length=1, default='K')
    banovan = models.BooleanField(db_column='Banovan', default=False)

    class Meta:
        db_table = 'uloga'


class Autor(Uloga):
    imeprezime = models.CharField(db_column='ImePrezime', max_length=40)
    datumrodjenja = models.DateField(db_column='DatumRodjenja')
    biografija = models.CharField(db_column='Biografija', max_length=1000)

    class Meta:
        db_table = 'autor'


class Korisnik(Uloga):
    imeprezime = models.CharField(db_column='ImePrezime', max_length=40)
    datumrodjenja = models.DateField(db_column='DatumRodjenja')

    class Meta:
        db_table = 'korisnik'


class IzdavackaKuca(Uloga):
    naziv = models.CharField(db_column='Naziv', max_length=40)
    istorija = models.CharField(db_column='Istorija', max_length=1000, blank=True, null=True)
    adresa = models.CharField(db_column='Adresa', max_length=60)

    class Meta:
        db_table = 'izdavackakuca'


class Knjiga(models.Model):
    isbn = models.CharField(db_column='ISBN', primary_key=True, max_length=20)
    naziv = models.CharField(db_column='Naziv', max_length=40)
    slika = models.ImageField(db_column='Slika', null=True, upload_to='knjigaImgs/')
    opis = models.CharField(db_column='Opis', max_length=100, blank=True, null=True)
    prosecnaocena = models.DecimalField(db_column='ProsecnaOcena', max_digits=5, decimal_places=2)
    idizdkuca = models.ForeignKey(db_column='IDIzdKuca', max_length=20, to='IzdavackaKuca', on_delete=models.CASCADE)

    class Meta:
        db_table = 'knjiga'


class Kolekcija(models.Model):
    korime = models.ForeignKey(db_column='KorIme', max_length=20, to='Uloga', on_delete=models.CASCADE)
    isbn = models.ForeignKey(db_column='ISBN', max_length=20, to='Knjiga', on_delete=models.CASCADE)

    class Meta:
        db_table = 'kolekcija'
        unique_together = ('korime', 'isbn')


class Licitacija(models.Model):
    idlicitacija = models.AutoField(db_column='IDLicitacija', primary_key=True)
    nazivdela = models.CharField(db_column='NazivDela', max_length=40)
    pdf = models.FileField(db_column='PDF', upload_to='pdfs/', null=True)
    datumpocetka = models.DateTimeField(db_column='DatumPocetka')
    datumkraja = models.DateTimeField(db_column='DatumKraja')
    pocetnacena = models.IntegerField(db_column='PocetnaCena')
    trenutniiznos = models.IntegerField(db_column='TrenutniIznos')
    idautor = models.ForeignKey(db_column='IDAutor', max_length=20, to='Autor', on_delete=models.CASCADE)
    idpobednik = models.ForeignKey(db_column='IDPobednik', max_length=20, blank=True, null=True, to='IzdavackaKuca', on_delete=models.CASCADE)

    class Meta:
        db_table = 'licitacija'


class NajpopularnijiMesec(models.Model):
    idocenjenog = models.CharField(db_column='IDOcenjenog', primary_key=True, max_length=20)
    prosecnaocena = models.DecimalField(db_column='ProsecnaOcena', max_digits=5, decimal_places=2)
    tip = models.CharField(db_column='Tip', max_length=1)

    class Meta:
        db_table = 'najpopularnijimesec'


class Napisao(models.Model):
    idautor = models.ForeignKey(db_column='IDAutor', max_length=20, to='Autor', on_delete=models.CASCADE)
    isbn = models.ForeignKey(db_column='ISBN', max_length=20, to='Knjiga', on_delete=models.CASCADE)

    class Meta:
        db_table = 'napisao'
        unique_together = ('idautor', 'isbn')


class Objava(models.Model):
    idobjava = models.AutoField(db_column='IDObjava', primary_key=True)
    sadrzaj = models.CharField(db_column='Sadrzaj', max_length=1000)
    datumobjave = models.DateTimeField(db_column='DatumObjave')
    slika = models.ImageField(db_column='Slika', upload_to='objavaImgs/', null=True)
    korime = models.ForeignKey(db_column='KorIme', max_length=20, to='Uloga', on_delete=models.CASCADE)

    class Meta:
        db_table = 'objava'


class Ponuda(models.Model):
    idponuda = models.AutoField(db_column='IDPonuda', primary_key=True)
    iznos = models.IntegerField(db_column='Iznos')
    idlicitacija = models.ForeignKey(db_column='IDLicitacija', to='Licitacija', on_delete=models.CASCADE)
    idizdkuca = models.ForeignKey(db_column='IDIzdKuca', max_length=20, to='IzdavackaKuca', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ponuda'


class Povezani(models.Model):
    idautor = models.ForeignKey(db_column='IDAutor', max_length=20, to='Autor', on_delete=models.CASCADE)
    idizdkuca = models.ForeignKey(db_column='IDIzdKuca', max_length=20, to='IzdavackaKuca', on_delete=models.CASCADE)

    class Meta:
        db_table = 'povezani'
        unique_together = ('idautor', 'idizdkuca')


class Prati(models.Model):
    idpratilac = models.ForeignKey(db_column='IDPratilac', max_length=20, to='Uloga', on_delete=models.CASCADE, related_name='related_to_pratilac')
    idpracen = models.ForeignKey(db_column='IDPracen', max_length=20, to='Uloga', on_delete=models.CASCADE, related_name='related_to_pracen')

    class Meta:
        db_table = 'prati'
        unique_together = ('idpratilac', 'idpracen')


class ProdajnaMesta(models.Model):
    idizdkuca = models.ForeignKey(db_column='IDIzdKuca', max_length=20, to='IzdavackaKuca', on_delete=models.CASCADE)
    adresa = models.CharField(db_column='Adresa', max_length=60)

    class Meta:
        db_table = 'prodajnamesta'
        unique_together = ('idizdkuca', 'adresa')


class Recenzija(models.Model):
    idrec = models.AutoField(db_column='IDRec', primary_key=True)
    ocena = models.DecimalField(db_column='Ocena', max_digits=5 ,decimal_places=1)
    datumobjave = models.DateTimeField(db_column='DatumObjave', auto_now_add=True)
    tekst = models.CharField(db_column='Tekst', max_length=1000)
    iddavalac = models.ForeignKey(db_column='IDDavalac', max_length=20, to='Uloga', on_delete=models.CASCADE, related_name='related_to_davalac_uloga')
    idprimalaculoga = models.ForeignKey(db_column='IDPrimalacUloga', max_length=20, blank=True, null=True, to='Uloga', on_delete=models.CASCADE, related_name='related_to_primalac_uloga')
    idprimalacknjiga = models.ForeignKey(db_column='IDPrimalacKnjiga', max_length=20, blank=True, null=True, to='Knjiga', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recenzija'
