from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.models import Group
from django.db.models import Q, Max
from django.http import HttpRequest, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from datetime import datetime
import random
import string
from django.core.mail import send_mail


# Create your views here.
def index(request: HttpRequest):
    feed = []
    knjige = [Knjiga.objects.get(pk=naj.idocenjenog) for naj in
              NajpopularnijiMesec.objects.filter(tip='K').order_by('-prosecnaocena')]
    autori = [Autor.objects.get(username=naj.idocenjenog) for naj in
              NajpopularnijiMesec.objects.filter(tip='A').order_by('-prosecnaocena')]
    kuce = [IzdavackaKuca.objects.get(username=naj.idocenjenog) for naj in
            NajpopularnijiMesec.objects.filter(tip='I').order_by('-prosecnaocena')]
    if request.user.is_authenticated:
        pracenja = Prati.objects.filter(idpratilac=request.user.pk)
        for pracenje in pracenja:
            objave = Objava.objects.filter(korime=pracenje.idpracen)
            feed.extend(objave)
    context = {
        'knjige': knjige,
        'autori': autori,
        'kuce': kuce,
        'pretragaForm': SearchForm(),
        'feed': feed
    }
    return render(request, 'index.html', context)


def generisiMesec(request: HttpRequest):
    NajpopularnijiMesec.objects.all().delete()

    for k in Knjiga.objects.all().order_by('-prosecnaocena')[0:3]:
        NajpopularnijiMesec.objects.create(idocenjenog=k.isbn, prosecnaocena=k.prosecnaocena, tip='K')

    for a in Autor.objects.all().order_by('-prosecnaocena')[0:3]:
        NajpopularnijiMesec.objects.create(idocenjenog=a.username, prosecnaocena=a.prosecnaocena, tip='A')

    for i in IzdavackaKuca.objects.all().order_by('-prosecnaocena')[0:3]:
        NajpopularnijiMesec.objects.create(idocenjenog=i.username, prosecnaocena=i.prosecnaocena, tip='I')

    return HttpResponse("Generisano <3")


def reg(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'registration/reg.html', {
        'pretragaForm': SearchForm()
    })


def regKorisnik(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    form = KorisnikRegForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user: Korisnik = form.save(commit=False)
        user.imeprezime = form.cleaned_data["ime"] + " " + form.cleaned_data["prezime"]
        user.save()
        group = Group.objects.get(name='Korisnici')
        user.groups.add(group)
        login(request, user)
        return redirect('home')
    return render(request, 'registration/regKorisnik.html', {
        'form': form,
        'pretragaForm': SearchForm()
    })


def regAutor(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    form = AutorRegForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user: Autor = form.save(commit=False)
        user.tip = 'A'
        user.imeprezime = form.cleaned_data["ime"] + " " + form.cleaned_data["prezime"]
        user.save()
        group = Group.objects.get(name='Autori')
        user.groups.add(group)
        login(request, user)
        return redirect('home')
    return render(request, 'registration/regAutor.html', {
        'form': form,
        'pretragaForm': SearchForm()
    })


def regKuca(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    form = KucaRegForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user: IzdavackaKuca = form.save(commit=False)
        user.tip = 'I'
        user.save()
        group = Group.objects.get(name='Kuce')
        user.groups.add(group)
        lokacije = form.cleaned_data["lokacije"].split("#")
        for lok in lokacije:
            if lok:
                instance = ProdajnaMesta(idizdkuca=user, adresa=lok)
                instance.save()
        login(request, user)
        return redirect('home')
    return render(request, 'registration/regKuca.html', {
        'form': form,
        'pretragaForm': SearchForm()
    })


def login_req(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html", {
        "form": form,
        'pretragaForm': SearchForm()
    })


def logout_req(request: HttpRequest):
    logout(request)
    return redirect('home')


def knjiga(request: HttpRequest, knjiga_id: str):
    try:
        # messages.clear(request)
        form = RecenzijaForm(data=request.POST or None)
        editForm = RecenzijaEditForm(data=request.POST or None)
        knjiga = Knjiga.objects.get(isbn=knjiga_id)
        napisanija = Napisao.objects.filter(isbn=knjiga_id)
        autori = ''
        for napisanije in napisanija:
            autori += napisanije.idautor.imeprezime + ', '
        autori = autori[0:-2]
        errorTekst=None
        recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga_id)

        imaUkolekciji=False
        korisnik = Uloga.objects.get(username=request.user.get_username())
        tmpKolekcije=Kolekcija.objects.filter(isbn=knjiga).filter(korime=korisnik)

        if(tmpKolekcije.count()!=0):
            imaUkolekciji=True

        #if Recenzija.objects.get(iddavalac=request.user):
           # TODO @ljubica IZBACI GRESKU - ne mogu da dam dve recenzije na nesto!

        if "dodajUkolekciju" in request.POST:
            kolekcija = Kolekcija(isbn=knjiga, korime=korisnik)
            kolekcija.save()
            imaUkolekciji = True

        if "brisiIzKolekcije" in request.POST:
            tmpKolekcije.delete()
            imaUkolekciji = False
    except Knjiga.DoesNotExist:
        raise Http404("Ne postoji knjiga sa tim ID :(")
    except Recenzija.DoesNotExist:
        raise Http404("Ne postoji knjiga sa tim ID :(")

    if form.is_valid():
        if "postavi" in request.POST:
            datum = datetime.now()
            ocena = form.cleaned_data["ocena"]
            tekst = form.cleaned_data["tekst"]

            rec = Recenzija.objects.filter(idprimalacknjiga=knjiga).filter(iddavalac=korisnik)
            if(rec.count()==0):
                # TODO @ljubica mozemo da promenimo model da polje bude models.AutoField i onda auto generise
                poslRec = Recenzija.objects.last()
                poslId = 0
                if (poslRec):
                    poslId = poslRec.idrec
                novId = poslId + 1
                novaRec = Recenzija(idrec=novId, ocena=ocena, datumobjave=datum, tekst=tekst, iddavalac=korisnik,
                                    idprimalacknjiga=knjiga)
                novaRec.save()
                recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga)
                sumaOcena = 0
                for rec in recenzije:
                    sumaOcena = sumaOcena + rec.ocena

                prosecnaOcena = sumaOcena / recenzije.count()

                knjiga.prosecnaocena = round(prosecnaOcena, 2)
                knjiga.save()
            else:
                errorTekst= 'Ne mozete upisati više od 1 recenzije!'
    if editForm.is_valid():
        if "izmeni" in request.POST:
            ocena = form.cleaned_data["ocena"]
            tekst = form.cleaned_data["tekst"]
            idRec = request.POST.get('hiddenIdRec')
            novaRec = Recenzija.objects.get(idrec=idRec)
            novaRec.ocena = ocena
            novaRec.datumobjave = datetime.now()
            novaRec.tekst = tekst
            novaRec.save()
            recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga)
            sumaOcena = 0
            for rec in recenzije:
                sumaOcena = sumaOcena + rec.ocena

            prosecnaOcena = sumaOcena / recenzije.count()

            knjiga.prosecnaocena = round(prosecnaOcena, 2)
            knjiga.save()
        if "obrisi" in request.POST:
            idRec = request.POST.get('hiddenIdRec')
            novaRec = Recenzija.objects.get(idrec=idRec)
            novaRec.delete()
            recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga)
            sumaOcena = 0
            for rec in recenzije:
                sumaOcena = sumaOcena + rec.ocena

            prosecnaOcena = sumaOcena / recenzije.count()

            knjiga.prosecnaocena = round(prosecnaOcena, 2)
            knjiga.save()

    context = {
        'knjiga': knjiga,
        'autori': autori,
        'recenzije': recenzije,
        'forma': form,
        'editForma': editForm,
        'pretragaForm': SearchForm(),
        'errorTekst':errorTekst,
        'imaUkolekciji':imaUkolekciji,
    }
    return render(request, 'entities/knjiga.html', context)


def profil(request: HttpRequest, profil_id: str):
    try:
        uloga = Uloga.objects.get(pk=profil_id)
        flag = 0
        recenzije = Recenzija.objects.filter(idprimalaculoga=uloga)
        objave = Objava.objects.filter(korime=uloga)

        if (request.user.is_authenticated and request.user!=uloga):
            if(Prati.objects.filter(idpracen=uloga, idpratilac=request.user).exists()):
                flag = 2
            else:
                flag = 1

        context = {
            'uloga': uloga,
            'recenzije': recenzije,
            'objave': objave,
            'pretragaForm': SearchForm(),
            'objavaForm': TextObjavaForm(),
            'knjigaForm': KnjigaObjavaForm(),
            'flag': flag
        }


        if uloga.tip == 'A':
            autor: Autor=Autor.objects.get(pk=profil_id)
            context['profil'] = autor
            context['knjige'] = Knjiga.objects.filter(napisao__idautor=profil_id).order_by('-prosecnaocena')
            context['licna_kolekcija']=Knjiga.objects.filter(kolekcija__korime=autor)
            return render(request, 'entities/autor.html', context)
        elif uloga.tip == 'K':
            korisnik: Korisnik=Korisnik.objects.get(pk=profil_id)
            context['profil'] = korisnik
            context['licna_kolekcija']=Knjiga.objects.filter(kolekcija__korime=korisnik)
            return render(request, 'entities/korisnik.html', context)
        else:
            context['profil'] = IzdavackaKuca.objects.get(pk=profil_id)
            return render(request, 'entities/izdavackakuca.html', context)
    except Autor.DoesNotExist:
        raise Http404("Ne postoji profil sa tim ID :(")


@login_required(login_url="login")
def mojProfil(request: HttpRequest):
    return redirect("profil", profil_id=request.user.username)


@login_required(login_url="login")
def promeniSifru(request: HttpRequest):
    form = PromenaSifreForm(request.POST or None)
    message = ""
    if form.is_valid():
        pass1 = form.cleaned_data["password1"]
        pass2 = form.cleaned_data["password2"]
        if pass1 == pass2:
            request.user.set_password(pass1)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect("mojProfil")
        else:
            message = "Lozinke se ne poklapaju"
    else:
        form = PromenaSifreForm()
    return render(request, "entities/promenaLozinke.html", {
        "form": form,
        "message": message,
        'pretragaForm': SearchForm()
    })


@login_required(login_url="login")
def promeniInfo(request: HttpRequest):
    uloga: Uloga = Uloga.objects.get(pk=request.user.pk)
    if uloga.tip == 'K':
        korisnik: Korisnik = Korisnik.objects.get(pk=request.user.pk)
        rIndex = korisnik.imeprezime.index(" ")
        form = PromenaInfoKorisnikForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            korisnik.email = form.cleaned_data["email"]
            korisnik.imeprezime = form.cleaned_data["ime"] + " " + form.cleaned_data["prezime"]
            korisnik.datumrodjenja = form.cleaned_data["datumrodjenja"]
            if request.FILES:
                korisnik.slika = form.cleaned_data["slika"]
            korisnik.save()
            return redirect("mojProfil")
        else:
            form = PromenaInfoKorisnikForm(initial={
                "email": korisnik.email,
                "ime": korisnik.imeprezime[:rIndex],
                "prezime": korisnik.imeprezime[rIndex + 1:],
                "datumrodjenja": korisnik.datumrodjenja
            })
    elif uloga.tip == 'A':
        autor: Autor = Autor.objects.get(pk=request.user.pk)
        rIndex = autor.imeprezime.index(" ")
        form = PromenaInfoAutorForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            autor.email = form.cleaned_data["email"]
            autor.imeprezime = form.cleaned_data["ime"] + " " + form.cleaned_data["prezime"]
            autor.datumrodjenja = form.cleaned_data["datumrodjenja"]
            autor.biografija = form.cleaned_data["biografija"]
            if request.FILES:
                autor.slika = form.cleaned_data["slika"]
            autor.save()
            return redirect("mojProfil")
        else:
            form = PromenaInfoAutorForm(initial={
                "email": autor.email,
                "ime": autor.imeprezime[:rIndex],
                "prezime": autor.imeprezime[rIndex + 1:],
                "datumrodjenja": autor.datumrodjenja,
                "biografija": autor.biografija
            })
    else:
        kuca: IzdavackaKuca = IzdavackaKuca.objects.get(pk=request.user.pk)
        lokacijez = ProdajnaMesta.objects.filter(idizdkuca=kuca)
        lokacije = ""
        for lok in lokacijez:
            lokacije += lok.adresa + "#"
        lokacije = lokacije[:-1]
        form = PromenaInfoKucaForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            kuca.email = form.cleaned_data["email"]
            kuca.naziv = form.cleaned_data["naziv"]
            kuca.istorija = form.cleaned_data["istorija"]
            kuca.adresa = form.cleaned_data["adresa"]
            ProdajnaMesta.objects.filter(idizdkuca=kuca).delete()
            lokacijes = form.cleaned_data["lokacije"].split("#")
            for lok in lokacijes:
                if lok:
                    instance = ProdajnaMesta(idizdkuca=kuca, adresa=lok)
                    instance.save()
            if request.FILES:
                kuca.slika = form.cleaned_data["slika"]
            kuca.save()
            return redirect("mojProfil")
        else:
            form = PromenaInfoKucaForm(initial={
                "email": kuca.email,
                "naziv": kuca.naziv,
                "istorija": kuca.istorija,
                "adresa": kuca.adresa,
                "lokacije": lokacije
            })
    return render(request, "entities/promenaInfo.html", {
        "form": form,
        'pretragaForm': SearchForm()
    })


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


def posaljiMejlLozinka(lozinka, primalac):
    subject = "[Čitaj, ne skitaj] Vaša lozinka je uspešno resetovana"
    message = "Nova privremena lozinka: " + lozinka
    recipient_list = [primalac]
    from_email = "pp200023d@student.etf.bg.ac.rs"
    send_mail(subject, message, from_email, recipient_list)


def posaljiMejlBanovan(tekst, primalac):
    subject = "[Čitaj, ne skitaj] Nažalost, morali smo da onesposobimo Vaš nalog"
    message = "Zbog narušene politike našeg sajta, suspendovani ste sa istog.\n\n" + tekst
    recipient_list = [primalac]
    from_email = "pp200023d@student.etf.bg.ac.rs"
    send_mail(subject, message, from_email, recipient_list)


def admResetujLozinku(request: HttpRequest):
    form = AdminResetForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        uloga: Uloga = Uloga.objects.filter(Q(email=email) & Q(username=username)).first()
        if uloga:
            str = generate_random_string(10)
            uloga.set_password(str)
            uloga.save()
            form = AdminResetForm(initial={
                "username": username,
                "email": email,
                "sifra": str
            })
            # posaljiMejlLozinka(str, email)
    else:
        form = AdminResetForm()
    return render(request, "entities/adminPanel.html", {
        "form": form,
        'pretragaForm': SearchForm()
    })


def admBanujNalog(request: HttpRequest):
    form = AdminBanForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        uloga: Uloga = Uloga.objects.filter(Q(email=email) & Q(username=username)).first()
        if uloga:
            uloga.is_active = 0
            uloga.banovan = 1
            uloga.save()
            # posaljiMejlBanovan(form.cleaned_data["tekst"], email)
            return redirect("mojProfil")
    else:
        form = AdminBanForm()
    return render(request, "entities/adminPanel.html", {
        "form": form,
        'pretragaForm': SearchForm()
    })


def pretraga(request: HttpRequest):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        naziv = form.cleaned_data["naziv"]
        tip = form.cleaned_data["tip"]
        znak = ("-" if form.cleaned_data["filter"] == "Ocena opadajuće" else "")
        objekti = []
        if tip == "Knjiga" or tip == "Sve":
            objektiz = Knjiga.objects.filter(Q(naziv__icontains=naziv)).order_by(znak + 'prosecnaocena')
            for obj in objektiz:
                objekti.append({
                    "tip": "knjiga",
                    "id": obj.isbn,
                    "slika": obj.slika,
                    "prosecnaocena": obj.prosecnaocena,
                    "naziv": obj.naziv
                })
        if tip == "Korisnik" or tip == "Sve":
            objektiz = Korisnik.objects.filter(Q(imeprezime__icontains=naziv)).order_by(znak + 'prosecnaocena')
            for obj in objektiz:
                objekti.append({
                    "tip": "profil",
                    "id": obj.username,
                    "slika": obj.slika,
                    "prosecnaocena": obj.prosecnaocena,
                    "naziv": obj.imeprezime
                })
        if tip == "Kuća" or tip == "Sve":
            objektiz = IzdavackaKuca.objects.filter(Q(naziv__icontains=naziv)).order_by(znak + 'prosecnaocena')
            for obj in objektiz:
                objekti.append({
                    "tip": "profil",
                    "id": obj.username,
                    "slika": obj.slika,
                    "prosecnaocena": obj.prosecnaocena,
                    "naziv": obj.naziv
                })
        if tip == "Autor" or tip == "Sve":
            objektiz = Autor.objects.filter(Q(imeprezime__icontains=naziv)).order_by(znak + 'prosecnaocena')
            for obj in objektiz:
                objekti.append({
                    "tip": "profil",
                    "id": obj.username,
                    "slika": obj.slika,
                    "prosecnaocena": obj.prosecnaocena,
                    "naziv": obj.imeprezime
                })
        return render(request, "entities/pretraga.html", {
            'pretragaForm': form,
            'objekti': objekti
        })
    else:
        return redirect(request.META.get("HTTP_REFERER"))


@login_required(login_url="login")
def zaprati(request: HttpRequest):
    if(request.method == 'POST'):
        form = PretplataForm(request.POST)
        if form.is_valid():

            pratilac = request.user

            praceni_id = request.POST.get('praceni')
            praceni = Uloga.objects.get(pk=praceni_id)
            praceni.brpratilaca += 1
            praceni.save()

            Prati.objects.create(idpracen=praceni, idpratilac=pratilac)

            return redirect('profil', praceni_id)

    return redirect('home')

@login_required(login_url="login")
def otprati(request:HttpRequest):
    if (request.method == 'POST'):
        form = PretplataForm(request.POST)
        if form.is_valid():
            pratilac = request.user

            praceni_id = request.POST.get('praceni')
            praceni = Uloga.objects.get(pk=praceni_id)
            praceni.brpratilaca -= 1
            praceni.save()

            Prati.objects.get(idpracen=praceni, idpratilac=pratilac).delete()
            return redirect('profil', praceni_id)
    return redirect('home')


def procitajISBN():
    with open('static/ISBN.txt', 'r') as file:
        return file.read().strip()


def upisiISBN(novISBN):
    with open('static/ISBN.txt', 'w') as file:
        file.write(novISBN)


def generisiISBN():
    ISBN = str(int(procitajISBN()) + 1).zfill(13)
    upisiISBN(ISBN)
    return ISBN


@login_required(login_url="login")
def dodajObjavu(request: HttpRequest):
    form = TextObjavaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        id = Objava.objects.aggregate(max_idobjava=Max('idobjava'))['max_idobjava'] + 1
        sadrzaj = form.cleaned_data["sadrzaj"]
        slika = form.cleaned_data["slika"]
        datum = datetime.now()
        Objava(idobjava=id, sadrzaj=sadrzaj, datumobjave=datum, slika=slika, korime=request.user).save()
    return redirect("mojProfil")


@login_required(login_url="login")
def dodajKnjigu(request: HttpRequest):
    print("jajaKnjiga")
    pass
