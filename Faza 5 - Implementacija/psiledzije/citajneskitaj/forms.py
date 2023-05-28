from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, UserChangeForm
from django.forms import *
from .models import *


class KorisnikRegForm(UserCreationForm):
    email = EmailField(label="Email")
    username = CharField(label='Korisničko ime')
    password1 = CharField(label="Lozinka", strip=False, widget=PasswordInput())
    password2 = CharField(label="Ponovo lozinka", strip=False, widget=PasswordInput())
    ime = CharField(label='Ime')
    prezime = CharField(label='Prezime')
    datumrodjenja = DateField(label='Datum rodjenja', widget=DateInput(attrs={'type': 'date'}))
    slika = ImageField(label='Profilna slika', required=False)

    class Meta:
        model = Korisnik
        fields = ["email", "username", "password1", "password2", "ime", "prezime", "datumrodjenja", "slika"]


class AutorRegForm(KorisnikRegForm):
    biografija = CharField(label='Biografija', widget=Textarea)

    class Meta:
        model = Autor
        fields = ["email", "username", "password1", "password2", "ime", "prezime", "datumrodjenja", "slika", 'biografija']


class KucaRegForm(UserCreationForm):
    email = EmailField(label="Email")
    username = CharField(label='Korisničko ime')
    password1 = CharField(label="Lozinka", strip=False, widget=PasswordInput())
    password2 = CharField(label="Ponovo lozinka", strip=False, widget=PasswordInput())
    naziv = CharField(label='Naziv')
    slika = ImageField(label='Profilna slika', required=False)
    istorija = CharField(label='Istorija', widget=Textarea, required=False)
    adresa = CharField(label='Adresa')
    lokacije = CharField(label='Lokacije', required=False)

    class Meta:
        model = IzdavackaKuca
        fields = ["email", "username", "password1", "password2", "naziv", "slika", "istorija", "adresa", "lokacije"]


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=TextInput(attrs={"autofocus": True}), label="Korisničko ime")
    password = CharField(
        label="Lozinka",
        strip=False,
        widget=PasswordInput(),
    )


class PromenaSifreForm(Form):
    password1 = CharField(label="Lozinka", strip=False, widget=PasswordInput())
    password2 = CharField(label="Ponovo lozinka", strip=False, widget=PasswordInput())


class PromenaInfoKorisnikForm(ModelForm):
    email = EmailField(label="Email")
    ime = CharField(label='Ime')
    prezime = CharField(label='Prezime')
    datumrodjenja = DateField(label='Datum rodjenja', widget=DateInput(attrs={'type': 'date'}))
    slika = ImageField(label='Profilna slika', required=False)

    class Meta:
        model = Korisnik
        fields = ["email", "ime", "prezime", "datumrodjenja", "slika"]


class PromenaInfoAutorForm(PromenaInfoKorisnikForm):
    biografija = CharField(label='Biografija', widget=Textarea)

    class Meta:
        model = Autor
        fields = ["email", "ime", "prezime", "datumrodjenja", "slika", 'biografija']


class PromenaInfoKucaForm(ModelForm):
    email = EmailField(label="Email")
    naziv = CharField(label='Naziv')
    slika = ImageField(label='Profilna slika', required=False)
    istorija = CharField(label='Istorija', widget=Textarea, required=False)
    adresa = CharField(label='Adresa')
    lokacije = CharField(label='Lokacije', required=False)

    class Meta:
        model = IzdavackaKuca
        fields = ["email", "naziv", "slika", "istorija", "adresa", "lokacije"]