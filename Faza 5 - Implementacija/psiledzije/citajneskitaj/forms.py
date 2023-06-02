from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.core.validators import MinValueValidator
from django.forms import *
from .models import *
from django import forms

'''
Autori: 
- Predrag Pešić 0023/2020
- Aleksa Mićanović 0282/2020
- Luka Nevajda 0370/2020
- Ljubica Muravljov 0071/2020
'''

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
    ban = ChoiceField(label="Akcija", widget=RadioSelect, choices=[("Ban", "Ban"), ("Unban", "Unban")], initial="Ban")
    tekst = CharField(label="Razlog (un)banovanja", widget=Textarea)


class SearchForm(Form):
    tipChoices = [("Sve", "Sve"), ("Knjiga", "Knjiga"), ("Korisnik", "Korisnik"), ("Kuća", "Kuća"), ("Autor", "Autor")]
    filterChoices = [("Ocena opadajuće", "Ocena opadajuće"), ("Ocena rastuće", "Ocena rastuće")]
    naziv = fields.CharField(widget=TextInput(attrs={"style": "float:left; height:38px;", "placeholder": "Pretraga...", "autocomplete": "off"}), required=False)
    tip = fields.ChoiceField(choices=tipChoices, widget=Select(attrs={"class": "form-select", "style": "width:fit-content; float:left;"}))
    filter = fields.ChoiceField(choices=filterChoices, widget=Select(attrs={"class": "form-select", "style": "width:fit-content; float:left; height:fit-content;"}))


class PretplataForm(Form):
    praceni = forms.CharField(widget=forms.HiddenInput(), max_length=30)


class TextObjavaForm(ModelForm):
    slika = ImageField(label='Slika objave (opciono)', required=False)
    sadrzaj = CharField(label='Sadrzaj', widget=Textarea)

    class Meta:
        model = Objava
        fields = ["slika", "sadrzaj"]
class AutoriField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.imeprezime}-[@{obj.username}]"

class KnjigaObjavaForm(ModelForm):
    naziv = CharField(label='Naziv knjige', widget=TextInput(attrs={"size": "50"}))
    slika = ImageField(label='Slika knjige', required=False)
    autori = AutoriField(queryset=Autor.objects.all(), widget=SelectMultiple(attrs={"class": "form-control"}))
    opis = CharField(label='Opis', widget=Textarea)
    sadrzaj = CharField(label='Sadržaj objave za knjigu', widget=Textarea)
    class Meta:
        model = Knjiga
        fields = ["naziv", "slika", "autori", "opis"]

class LicitacijaPonudaForm(Form):
    hiddenIdLic = forms.CharField(widget=forms.HiddenInput(), required=False, initial=-1)
    iznos = IntegerField(label='Iznos', required=True, min_value=1)


class DodajLicitacijuForm(Form):
    nazivdela = CharField(label='Naziv dela', widget=TextInput(attrs={"size": "50"}))
    pdf = FileField(label="PDF")
    datumkraja = forms.DateTimeField(
        label='Datum kraja',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    pocetnacena = IntegerField(label="Pocetna cena", validators=[
        MinValueValidator(1, message='Morate uneti vrednost veću od 0 kao početnu cenu.')
    ])
