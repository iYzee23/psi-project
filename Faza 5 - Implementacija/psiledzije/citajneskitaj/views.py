from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.models import Group
from django.http import HttpRequest, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from datetime import datetime

# Create your views here.
def index(request: HttpRequest):
    knjige = [Knjiga.objects.get(pk=naj.idocenjenog) for naj in NajpopularnijiMesec.objects.filter(tip='K').order_by('-prosecnaocena')]
    autori = [Autor.objects.get(username=naj.idocenjenog) for naj in NajpopularnijiMesec.objects.filter(tip='A').order_by('-prosecnaocena')]
    kuce = [IzdavackaKuca.objects.get(username=naj.idocenjenog) for naj in NajpopularnijiMesec.objects.filter(tip='I').order_by('-prosecnaocena')]
    context = {
        'knjige': knjige,
        'autori': autori,
        'kuce': kuce
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
    return render(request, 'registration/reg.html', {})


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
        'form': form
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
        'form': form
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
        'form': form
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
        "form": form
    })


def logout_req(request: HttpRequest):
    logout(request)
    return redirect('home')


def knjiga(request: HttpRequest, knjiga_id: str):
    try:
        form = RecenzijaForm(data=request.POST or None);
        editForm= RecenzijaEditForm(data=request.POST or None);
        knjiga2 = Knjiga.objects.get(pk=knjiga_id)
        knjiga2.opis="Zivot Ane Karenjine"
        knjiga2.save()
        napisanija = Napisao.objects.filter(isbn=knjiga2.isbn)
        autori = ''
        for napisanije in napisanija:
            autori += napisanije.idautor.imeprezime + ', '
        autori = autori[0:-2]

        recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga2)

    except:
        raise Http404("Ne postoji knjiga sa tim ID :(")


    if form.is_valid():

        if "postavi"  in request.POST:
            datum=datetime.now()
            ocena = form.cleaned_data["ocena"]
            tekst = form.cleaned_data["tekst"]
            davalac= Uloga.objects.get(username=request.user.get_username())
            poslRec = Recenzija.objects.last()
            poslId=0
            if(poslRec):
                poslId=poslRec.idrec
            novId=poslId+1
            knjiga2 = Knjiga.objects.get(pk=knjiga_id)
            novaRec=Recenzija(idrec=novId,ocena=ocena,datumobjave=datum,tekst=tekst,iddavalac=davalac,idprimalacknjiga=knjiga2)
            novaRec.save()
            recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga2)
            sumaOcena=0
            for rec in recenzije:
                sumaOcena=sumaOcena+rec.ocena

            prosecnaOcena=sumaOcena/recenzije.count()

            knjiga2.prosecnaocena=round(prosecnaOcena, 2)
            knjiga2.save()
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
            recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga2)
            sumaOcena = 0
            for rec in recenzije:
                sumaOcena = sumaOcena + rec.ocena

            prosecnaOcena = sumaOcena / recenzije.count()

            knjiga2.prosecnaocena = round(prosecnaOcena, 2)
            knjiga2.save()
        if "obrisi" in request.POST:
            idRec = request.POST.get('hiddenIdRec')
            novaRec = Recenzija.objects.get(idrec=idRec)
            novaRec.delete()
            recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga2)
            sumaOcena = 0
            for rec in recenzije:
                sumaOcena = sumaOcena + rec.ocena

            prosecnaOcena = sumaOcena / recenzije.count()

            knjiga2.prosecnaocena = round(prosecnaOcena, 2)
            knjiga2.save()


    context = {
        'knjiga': knjiga2,
        'autori': autori,
        'recenzije': recenzije,
        'forma':form,
        'editForma':editForm,
    }
    return render(request, 'entities/knjiga.html', context)


def profil(request: HttpRequest, profil_id: str):
    try:
        uloga = Uloga.objects.get(pk=profil_id)
        recenzije = Recenzija.objects.filter(idprimalaculoga=uloga)

        context = {
            'uloga': uloga,
            'recenzije': recenzije
        }

        if uloga.tip == 'A':
            context['profil'] = Autor.objects.get(pk=profil_id)
            return render(request, 'entities/autor.html', context)
        elif uloga.tip == 'K':
            context['profil'] = Korisnik.objects.get(pk=profil_id)
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
def dodajObjavu(request: HttpRequest):
    pass


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
        "message": message
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
        "form": form
    })
