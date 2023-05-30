from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.forms import *
from .models import *
from django import forms


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
        fields = ["email", "username", "password1", "password2", "ime", "prezime", "datumrodjenja", "slika",
                  'biografija']


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


class RecenzijaForm(Form):
    tekst = forms.CharField(label='Review', widget=forms.Textarea, max_length=1000, required=True)
    ocena = forms.IntegerField(widget=forms.TextInput(attrs={'type': 'range', 'min': '1', 'max': '5'}))
    hiddenIdRec = forms.CharField(widget=forms.HiddenInput(), required=False, initial=-1)


class AdminResetForm(Form):
    username = CharField(label='Korisničko ime')
    email = EmailField(label="Email")
    sifra = CharField(label="Generisana šifra", disabled=True, required=False,
                      widget=TextInput(attrs={"style": "background-color: lightgray"}))


class AdminBanForm(Form):
    username = CharField(label='Korisničko ime')
    email = EmailField(label="Email")
    tekst = CharField(label="Razlog banovanja", widget=Textarea())


class SearchForm(Form):
    tipChoices = [("Sve", "Sve"), ("Knjiga", "Knjiga"), ("Korisnik", "Korisnik"), ("Kuća", "Kuća"), ("Autor", "Autor")]
    filterChoices = [("Ocena opadajuće", "Ocena opadajuće"), ("Ocena rastuće", "Ocena rastuće")]
    naziv = fields.CharField(
        widget=TextInput(attrs={"style": "float:left; height:38px;", "placeholder": "Pretraga..."}), required=False)
    tip = fields.ChoiceField(choices=tipChoices,
                             widget=Select(attrs={"class": "form-select", "style": "width:fit-content; float:left;"}))
    filter = fields.ChoiceField(choices=filterChoices, widget=Select(
        attrs={"class": "form-select", "style": "width:fit-content; float:left; height:fit-content;"}))


class PretplataForm(Form):
    praceni = forms.CharField(widget=forms.HiddenInput(), max_length=30)


class TextObjavaForm(ModelForm):
    slika = ImageField(label='Slika objave (opciono)', required=False)
    sadrzaj = CharField(label='Sadrzaj', widget=Textarea)

    class Meta:
        model = Objava
        fields = ["slika", "sadrzaj"]


class KnjigaObjavaForm(ModelForm):
    autorChoices = [(autor.username, autor.imeprezime + " [@" + autor.username + "]") for autor in Autor.objects.all()]

    naziv = CharField(label='Naziv knjige', widget=TextInput(attrs={"size": "50"}))
    slika = ImageField(label='Slika knjige')
    autor = ChoiceField(choices=autorChoices, widget=Select)
    opis = CharField(label='Opis', widget=Textarea)

    class Meta:
        model = Knjiga
        fields = ["naziv", "slika", "autor", "opis"]
