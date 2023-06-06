from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.models import Group
from django.db.models import Q, Max
from django.http import HttpRequest, Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from datetime import datetime as dt
from .forms import *
import random, string
from django.utils import timezone

'''
Autori: 
- Predrag Pešić 0023/2020
- Aleksa Mićanović 0282/2020
- Luka Nevajda 0370/2020
- Ljubica Muravljov 0071/2020
'''


# Dohvata najpopularnije knjige, autore i kuce - kao i feed za ulogovane korisnike
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
    if feed:
        feed.sort(key=lambda x: x.datumobjave,reverse=True)
    context = {
        'knjige': knjige,
        'autori': autori,
        'kuce': kuce,
        'pretragaForm': SearchForm(),
        'feed': feed
    }
    generisiMesec(request)
    return render(request, 'index.html', context)


# Pomocna funkcija za generisanje najbolje ocenjenih knjiga, autora i kuca u trenutku pokretanja
def generisiMesec(request: HttpRequest):
    NajpopularnijiMesec.objects.all().delete()

    for k in Knjiga.objects.all().order_by('-prosecnaocena')[0:3]:
        NajpopularnijiMesec.objects.create(idocenjenog=k.isbn, prosecnaocena=k.prosecnaocena, tip='K')

    for a in Autor.objects.all().order_by('-prosecnaocena')[0:3]:
        NajpopularnijiMesec.objects.create(idocenjenog=a.username, prosecnaocena=a.prosecnaocena, tip='A')

    for i in IzdavackaKuca.objects.all().order_by('-prosecnaocena')[0:3]:
        NajpopularnijiMesec.objects.create(idocenjenog=i.username, prosecnaocena=i.prosecnaocena, tip='I')



# render stranice za registraciju
def reg(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'registration/reg.html', {
        'pretragaForm': SearchForm()
    })


# render stranice za registraciju korisnika / registracija korisnika iz forme
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


# render stranice za registraciju autora / registracija autora iz forme
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


# render stranice za registraciju izdavacke kuce / registracija izdavacke kuce iz forme
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


# render stranice za login / autorizacija usera
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


# logout usera
def logout_req(request: HttpRequest):
    logout(request)
    return redirect('home')


# render stranice knjige - dohvatanje informacija o samoj knjizi, da li korisnik ima knjigu u kolekciji,
# dohvatanje recenzija, kao i obrada POST zahteva za ostavljanje, menjanje i brisanje recenzije
def knjiga(request: HttpRequest, knjiga_id: str):
    try:
        knjiga = Knjiga.objects.get(isbn=knjiga_id)
    except Knjiga.DoesNotExist:
        raise Http404("Ne postoji knjiga sa tim ID :(")

    recenzijaForm = RecenzijaForm(data=request.POST or None, prefix='edit')
    if not recenzijaForm.is_valid():
        recenzijaForm = RecenzijaForm(data=request.POST or None, prefix='add')
    autori = Autor.objects.filter(napisao__isbn=knjiga)
    errorTekst = None

    # provera da li je knjiga u kolekciji
    korisnik = request.user
    imaUkolekciji = Kolekcija.objects.filter(Q(isbn=knjiga) & Q(korime=korisnik)).exists()

    if imaUkolekciji and "brisiIzKolekcije" in request.POST:
        Kolekcija.objects.get(Q(isbn=knjiga) & Q(korime=korisnik)).delete()
        imaUkolekciji = False
    elif not imaUkolekciji and "dodajUkolekciju" in request.POST:
        Kolekcija.objects.create(isbn=knjiga, korime=korisnik)
        imaUkolekciji = True

    # ukoliko je forma validna, znaci da je korisnik POSTovao iz 'Dodaj' ili 'Izmeni' recenziju
    if recenzijaForm.is_valid():
        # ako je dodaj ili izmeni
        if "obrisi" not in request.POST:
            ocena = recenzijaForm.cleaned_data["ocena"]
            tekst = recenzijaForm.cleaned_data["tekst"]
            try:
                recenzija = Recenzija.objects.get(Q(idprimalacknjiga=knjiga) & Q(iddavalac=korisnik))
                if "postavi" in request.POST:
                    errorTekst = 'Ne mozete upisati više od 1 recenzije!'

            except:
                recenzija = Recenzija(idprimalacknjiga=knjiga, iddavalac=korisnik)

            if autori.filter(username=korisnik.username).exists() or knjiga.idizdkuca_id==korisnik.username:
                errorTekst = 'Ne mozete ostaviti recenziju na Vasoj knjizi!'

            if errorTekst is None:
                recenzija.tekst = tekst
                recenzija.ocena = ocena
                recenzija.save()
        # ako je obrisi (na recenziji ciji je korisnik autor)
        elif "obrisi" in request.POST:
            Recenzija.objects.get(Q(idprimalacknjiga=knjiga) & Q(iddavalac=korisnik)).delete()

        if errorTekst is None:
            recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga)
            if recenzije.count() == 0:
                prosecnaOcena = 0
            else:
                sumaOcena = 0
                for postojecaRecenzija in recenzije:
                    sumaOcena = sumaOcena + postojecaRecenzija.ocena
                prosecnaOcena = sumaOcena / recenzije.count()

            knjiga.prosecnaocena = round(prosecnaOcena, 2)
            knjiga.save()

    # ako je stiglo obrisi (od strane admina)
    elif "obrisi" in request.POST:
        idRec = request.POST.get('hiddenIdDeleteRec')
        Recenzija.objects.get(idrec=idRec).delete()

        if errorTekst is None:
            recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga)
            if recenzije.count() == 0:
                prosecnaOcena = 0
            else:
                sumaOcena = 0
                for postojecaRecenzija in recenzije:
                    sumaOcena = sumaOcena + postojecaRecenzija.ocena
                prosecnaOcena = sumaOcena / recenzije.count()

            knjiga.prosecnaocena = round(prosecnaOcena, 2)
            knjiga.save()

    # dohvatanje recenzija i stavljanje korisnikove recenzije kao prve
    try:
        recenzija = list(Recenzija.objects.get(Q(idprimalacknjiga=knjiga) & Q(iddavalac=korisnik)))
        recenzije = list(Recenzija.objects.filter(idprimalacknjiga=knjiga).exclude(recenzija))
        recenzije = recenzija + recenzije
    except:
        recenzije = Recenzija.objects.filter(idprimalacknjiga=knjiga)

    context = {
        'knjiga': knjiga,
        'autori': autori,
        'recenzije': recenzije,
        'recenzijaFormAdd': RecenzijaForm(prefix='add'),
        'recenzijaFormEdit': RecenzijaForm(prefix='edit'),
        'pretragaForm': SearchForm(),
        'errorTekst': errorTekst,
        'imaUkolekciji': imaUkolekciji,
    }

    request.session['isbn'] = knjiga_id
    return render(request, 'entities/knjiga.html', context)


# redner stranice profila - dohvatanje informacija o profilu,
# obrada zahteva za postavljanje, izmenu i brisanje recenzije,
# flag da li trenutni user prati profil koji pregleda,
# kao i da li je ovo profil od ulogovanog usera
def profil(request: HttpRequest, profil_id: str):
    try:
        recenzijaForm = RecenzijaForm(data=request.POST or None, prefix='edit')
        if not recenzijaForm.is_valid():
            recenzijaForm = RecenzijaForm(data=request.POST or None, prefix='add')
        uloga = Uloga.objects.get(pk=profil_id)
        korisnik = request.user
        flag = 0
        objave = Objava.objects.filter(korime=uloga).order_by('-datumobjave')
        errorTekst = None

        # provera da li je profil pracen od strane usera
        if request.user.is_authenticated and request.user != uloga:
            if Prati.objects.filter(idpracen=uloga, idpratilac=request.user).exists():
                flag = 2
            else:
                flag = 1

        # ukoliko je forma validna, znaci da je korisnik POSTovao iz 'Dodaj' ili 'Izmeni' recenziju
        if recenzijaForm.is_valid():
            if "obrisi" not in request.POST:
                # ako je dodaj ili izmeni
                ocena = recenzijaForm.cleaned_data["ocena"]
                tekst = recenzijaForm.cleaned_data["tekst"]
                try:
                    recenzija = Recenzija.objects.get(Q(idprimalaculoga=uloga) & Q(iddavalac=korisnik))
                    if "postavi" in request.POST:
                        errorTekst = 'Ne mozete upisati više od 1 recenzije!'

                except:
                    recenzija = Recenzija(idprimalaculoga=uloga, iddavalac=korisnik)

                if recenzija.idprimalaculoga==korisnik:
                    errorTekst = 'Ne mozete ostaviti recenziju sami sebi!'
                if errorTekst is None:
                    recenzija.tekst = tekst
                    recenzija.ocena = ocena
                    recenzija.save()
            # ako je obrisi (na recenziji ciji je korisnik autor)
            elif "obrisi" in request.POST:
                Recenzija.objects.get(Q(idprimalaculoga=uloga) & Q(iddavalac=korisnik)).delete()

            if errorTekst is None:
                recenzije = Recenzija.objects.filter(idprimalaculoga=uloga)
                if recenzije.count() == 0:
                    prosecnaOcena = 0
                else:
                    sumaOcena = 0
                    for postojecaRecenzija in recenzije:
                        sumaOcena = sumaOcena + postojecaRecenzija.ocena
                    prosecnaOcena = sumaOcena / recenzije.count()

                uloga.prosecnaocena = round(prosecnaOcena, 2)
                uloga.save()
        # ako je stiglo obrisi (od strane admina)
        elif "obrisi" in request.POST:
            idRec = request.POST.get('hiddenIdDeleteRec')
            Recenzija.objects.get(idrec=idRec).delete()

            if errorTekst is None:
                recenzije = Recenzija.objects.filter(idprimalaculoga=uloga)
                if recenzije.count() == 0:
                    prosecnaOcena = 0
                else:
                    sumaOcena = 0
                    for postojecaRecenzija in recenzije:
                        sumaOcena = sumaOcena + postojecaRecenzija.ocena
                    prosecnaOcena = sumaOcena / recenzije.count()

                uloga.prosecnaocena = round(prosecnaOcena, 2)
                uloga.save()

        # dohvatanje recenzija i stavljanje korisnikove recenzije kao prve
        try:
            recenzija = list(Recenzija.objects.get(Q(idprimalaculoga=uloga) & Q(iddavalac=korisnik)))
            recenzije = list(Recenzija.objects.filter(idprimalaculoga=uloga).exclude(recenzija))
            recenzije = recenzija + recenzije
        except:
            recenzije = Recenzija.objects.filter(idprimalaculoga=uloga)

        # generisanje listi pratilaca i pracenih
        pratioci = []
        praceni = []
        pratiociz = [pratilac.idpratilac for pratilac in Prati.objects.filter(idpracen_id=profil_id)]
        praceniz = [pracen.idpracen for pracen in Prati.objects.filter(idpratilac_id=profil_id)]
        for pratilac in pratiociz:
            pratioci.append({
                "username": pratilac.username,
                "slika": pratilac.slika,
                "naziv": Korisnik.objects.get(username=pratilac.username).imeprezime if pratilac.tip == "K"
                else (Autor.objects.get(username=pratilac.username).imeprezime if pratilac.tip == "A"
                      else IzdavackaKuca.objects.get(username=pratilac.username).naziv)
            })
        for pracen in praceniz:
            praceni.append({
                "username": pracen.username,
                "slika": pracen.slika,
                "naziv": Korisnik.objects.get(username=pracen.username).imeprezime if pracen.tip == "K"
                else (Autor.objects.get(username=pracen.username).imeprezime if pracen.tip == "A"
                      else IzdavackaKuca.objects.get(username=pracen.username).naziv)
            })

        context = {
            'uloga': uloga,
            'recenzije': recenzije,
            'objave': objave,
            'recenzijaFormAdd': RecenzijaForm(prefix='add'),
            'recenzijaFormEdit': RecenzijaForm(prefix='edit'),
            'pretragaForm': SearchForm(),
            'objavaForm': TextObjavaForm(),
            'objavaFormEdit': TextObjavaForm(prefix='objavaEdit'),
            'objavaFormDelete': ObjavaDeleteForm(),
            'knjigaForm': KnjigaObjavaForm(prefix='novaKnjiga'),
            'flag': flag,
            'errorTekst': errorTekst,
            'pratioci': pratioci,
            'praceni': praceni
        }

        if uloga.tip == 'A':
            autor: Autor = Autor.objects.get(pk=profil_id)
            context['profil'] = autor
            context['knjige'] = Knjiga.objects.filter(napisao__idautor=profil_id).order_by('-prosecnaocena')
            context['licna_kolekcija'] = Knjiga.objects.filter(kolekcija__korime=autor)
            context['kuce'] = IzdavackaKuca.objects.filter(povezani__idautor=autor).order_by(
                '-prosecnaocena').distinct()
            return render(request, 'entities/autor.html', context)
        elif uloga.tip == 'K':
            korisnik: Korisnik = Korisnik.objects.get(pk=profil_id)
            context['profil'] = korisnik
            context['licna_kolekcija'] = Knjiga.objects.filter(kolekcija__korime=korisnik)
            return render(request, 'entities/korisnik.html', context)
        else:
            kuca = IzdavackaKuca.objects.get(pk=profil_id)
            context['profil'] = kuca
            context['licna_kolekcija'] = Knjiga.objects.filter(kolekcija__korime=korisnik)
            context['knjige'] = Knjiga.objects.filter(idizdkuca=kuca).order_by('-prosecnaocena')
            context['autori'] = Autor.objects.filter(povezani__idizdkuca=kuca).order_by('imeprezime').distinct()
            context['lokacije'] = ProdajnaMesta.objects.filter(idizdkuca=profil_id)
            return render(request, 'entities/izdavackakuca.html', context)
    except Autor.DoesNotExist:
        raise Http404("Ne postoji profil sa tim ID :(")


# redirect na profil usera
@login_required(login_url="login")
def mojProfil(request: HttpRequest):
    return redirect("profil", profil_id=request.user.username)


# render stranice za promenu sifre / promena sifre u bazi
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


# menja informacija o profilu u bazi na osnovu POSTovane forme
# forme se razlikuju u zavisnosti od tipa profila
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


# pomocna funkcija za generisanje nove sifre na zahtev
def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string


# funkcija za slanje nove lozinke mailom
def posaljiMejlLozinka(lozinka, primalac):
    subject = "[Čitaj, ne skitaj] Vaša lozinka je uspešno resetovana"
    message = "Nova privremena lozinka: " + lozinka
    recipient_list = [primalac]
    from_email = "pp200023d@student.etf.bg.ac.rs"
    send_mail(subject, message, from_email, recipient_list)


# funkcija za slanje obavestenja o banovanju mailom
def posaljiMejlBanovan(tekst, primalac):
    subject = "[Čitaj, ne skitaj] Nažalost, morali smo da onesposobimo Vaš nalog"
    message = "Zbog narušene politike našeg sajta, suspendovani ste sa istog.\n\n" + tekst
    recipient_list = [primalac]
    from_email = "pp200023d@student.etf.bg.ac.rs"
    send_mail(subject, message, from_email, recipient_list)


# reset lozinke od strane admina - ukoliko se poklapaju uneti username i email, generise se nova lozinka
@login_required(login_url="login")
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


# banovanje / odbanovanje naloga od strane admina
@login_required(login_url="login")
def admBanujNalog(request: HttpRequest):
    form = AdminBanForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        email = form.cleaned_data["email"]
        ban = form.cleaned_data["ban"]
        uloga: Uloga = Uloga.objects.filter(Q(email=email) & Q(username=username)).first()
        if uloga:
            if ban == "Ban":
                uloga.is_active = 0
                uloga.banovan = 1
            else:
                uloga.is_active = 1
                uloga.banovan = 0
            uloga.save()
            # posaljiMejlBanovan(form.cleaned_data["tekst"], email)
            return redirect("mojProfil")
    else:
        form = AdminBanForm()
    return render(request, "entities/adminPanel.html", {
        "form": form,
        'pretragaForm': SearchForm()
    })


# izvrsavanje pretrage (forma u headeru) - u zavisnosti od kriterijuma prosledjuje rezultate
def pretraga(request: HttpRequest):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        naziv = form.cleaned_data["naziv"]
        tip = form.cleaned_data["tip"]
        znak = ("-" if form.cleaned_data["filter"] == "Ocena opadajuće" else "")
        objekti = []
        if tip == "Knjiga" or tip == "Sve":
            objektiz = Knjiga.objects.filter(Q(naziv__icontains=naziv) | Q(isbn__icontains=naziv)).order_by(znak + 'prosecnaocena')
            for obj in objektiz:
                objekti.append({
                    "tip": "knjiga",
                    "id": obj.isbn,
                    "slika": obj.slika,
                    "prosecnaocena": obj.prosecnaocena,
                    "naziv": obj.naziv
                })
        if tip == "Korisnik" or tip == "Sve":
            objektiz = Korisnik.objects.filter((Q(imeprezime__icontains=naziv) | Q(username__icontains=naziv)) & Q(is_active=1)).order_by(znak + 'prosecnaocena')
            for obj in objektiz:
                objekti.append({
                    "tip": "profil",
                    "id": obj.username,
                    "slika": obj.slika,
                    "prosecnaocena": obj.prosecnaocena,
                    "naziv": obj.imeprezime
                })
        if tip == "Kuća" or tip == "Sve":
            objektiz = IzdavackaKuca.objects.filter((Q(naziv__icontains=naziv) | Q(username__icontains=naziv)) & Q(is_active=1)).order_by(znak + 'prosecnaocena')
            for obj in objektiz:
                objekti.append({
                    "tip": "profil",
                    "id": obj.username,
                    "slika": obj.slika,
                    "prosecnaocena": obj.prosecnaocena,
                    "naziv": obj.naziv
                })
        if tip == "Autor" or tip == "Sve":
            objektiz = Autor.objects.filter((Q(imeprezime__icontains=naziv) | Q(username__icontains=naziv)) & Q(is_active=1)).order_by(znak + 'prosecnaocena')
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


# evidentira pracenje profila od strane usera
@login_required(login_url="login")
def zaprati(request: HttpRequest):
    if request.method == 'POST':
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


# evidentira odpracivanje profila od strane usera
@login_required(login_url="login")
def otprati(request: HttpRequest):
    if request.method == 'POST':
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


# pomocna funkcija za generisanje sledeceg ISBNa
def procitajISBN():
    with open('static/ISBN.txt', 'r') as file:
        return file.read().strip()


# pomocna funkcija za generisanje sledeceg  ISBNa
def upisiISBN(novISBN):
    with open('static/ISBN.txt', 'w') as file:
        file.write(novISBN)


# pomocna funkcija za generisanjes sledeceg ISBNa
def generisiISBN():
    ISBN = str(int(procitajISBN()) + 1).zfill(13)
    upisiISBN(ISBN)
    return ISBN


# dodaje objavu iz forme u bazu
@login_required(login_url="login")
def dodajObjavu(request: HttpRequest):
    izmenaForm = TextObjavaForm(request.POST or None, request.FILES or None)
    if izmenaForm.is_valid():
        # id = Objava.objects.aggregate(max_idobjava=Max('idobjava'))['max_idobjava'] + 1
        sadrzaj = izmenaForm.cleaned_data["sadrzaj"]
        slika = izmenaForm.cleaned_data["slika"]
        Objava(sadrzaj=sadrzaj, datumobjave=timezone.now(), slika=slika, korime=request.user).save()
    return redirect("mojProfil")

# menja objavu i dodaje je u bazu
@login_required(login_url="login")
def izmeniObjavu(request: HttpRequest):
    form = TextObjavaForm(request.POST or None, request.FILES or None, prefix='objavaEdit')
    if form.is_valid():
        id=form.cleaned_data["hiddenIdObjave"]
        sadrzaj = form.cleaned_data["sadrzaj"]
        slika = form.cleaned_data["slika"]
        objava = Objava.objects.get(idobjava=id)
        objava.datumobjave=timezone.now()
        objava.sadrzaj=sadrzaj
        if slika:
            objava.slika=slika
        objava.save()
    return redirect("mojProfil")

@login_required(login_url="login")
def obrisiObjavu(request: HttpRequest):
    form = ObjavaDeleteForm(request.POST or None)
    if form.is_valid():
        id=form.cleaned_data["hiddenIdObjave"]
        objava = Objava.objects.get(idobjava=id)
        objava.delete()
    return redirect(request.META.get("HTTP_REFERER"))



# dodaje knjigu iz forme u bazu
@login_required(login_url="login")
def dodajKnjigu(request: HttpRequest):
    form = KnjigaObjavaForm(request.POST or None, request.FILES or None, prefix='novaKnjiga')
    if form.is_valid():
        sadrzaj = form.cleaned_data["sadrzaj"]
        isbn = generisiISBN()
        naziv = form.cleaned_data["naziv"]
        slika = form.cleaned_data["slika"]
        print(slika)
        opis = form.cleaned_data["opis"]
        # autori = form.cleaned_data["autori"]
        autori = request.POST.getlist("mojiAutori")
        Knjiga(isbn=isbn, naziv=naziv, slika=slika, opis=opis, prosecnaocena=0, idizdkuca_id=request.user.pk).save()
        for autor in autori:
            Napisao(isbn_id=isbn, idautor_id=autor).save()
            if not Povezani.objects.filter(Q(idautor_id=autor) & Q(idizdkuca_id=request.user.pk)).exists():
                Povezani(idautor_id=autor, idizdkuca_id=request.user.pk).save()
        Objava(sadrzaj=sadrzaj, datumobjave=timezone.now(), slika=slika, korime=request.user).save()
    return redirect("mojProfil")


# dodaje promene knjige iz forme u bazu
@login_required(login_url="login")
def promeniInfoKnjige(request: HttpRequest):
    izd_kuca: IzdavackaKuca = IzdavackaKuca.objects.get(username=request.user.pk)
    knjiga: Knjiga = Knjiga.objects.get(isbn=request.session.get('isbn'))
    autori = Autor.objects.filter(napisao__isbn=knjiga)
    izmenaForm = KnjigaObjavaForm(request.POST or None, request.FILES or None)
    if izmenaForm.is_valid():
        sadrzaj = izmenaForm.cleaned_data["sadrzaj"]
        slika = izmenaForm.cleaned_data["slika"]
        knjiga.naziv = izmenaForm.cleaned_data["naziv"]
        knjiga.opis = izmenaForm.cleaned_data["opis"]
        if request.FILES:
            knjiga.slika = slika

        # novi_autori_id = izmenaForm.cleaned_data["autori"]
        novi_autori_id = request.POST.getlist("mojiAutoriOpet")

        for autor in autori:
            num_knjiga_autora_i_izd_kuce = Knjiga.objects.filter(
                Q(idizdkuca=izd_kuca) & Q(napisao__idautor=autor)).count()
            if num_knjiga_autora_i_izd_kuce == 1:
                Povezani.objects.get(idizdkuca=izd_kuca, idautor=autor).delete()
            Napisao.objects.get(idautor=autor, isbn=knjiga).delete()
        for novi_autor_id in novi_autori_id:
            novi_autor = Autor.objects.get(username=novi_autor_id)
            Napisao(idautor=novi_autor, isbn=knjiga).save()
            if not Povezani.objects.filter(Q(idautor=novi_autor) & Q(idizdkuca_id=request.user.pk)).exists():
                Povezani(idautor=novi_autor, idizdkuca_id=request.user.pk).save()
        knjiga.save()
        Objava(sadrzaj=sadrzaj, datumobjave=timezone.now(), slika=slika, korime=request.user).save()
        return redirect("knjiga", knjiga_id=knjiga.pk)
    else:
        print('Djoka')
        izmenaForm = KnjigaObjavaForm(initial={
            "naziv": knjiga.naziv,
            #"autori": autori,
            #"slika": knjiga.slika,
            "opis": knjiga.opis
        })
    return render(request, "entities/promenaInfoKnjige.html", {
        "form": izmenaForm,
        "sviAutori": autori
    })


@login_required(login_url="login")
def licitacije(request: HttpRequest):
    autor: Autor = Autor.objects.filter(username=request.user.pk).first()
    izd_kuca: IzdavackaKuca=IzdavackaKuca.objects.filter(username=request.user.pk).first()
    errorTekst = None
    form = LicitacijaPonudaForm(request.POST or None)

    if form.is_valid():
        iznos = form.cleaned_data['iznos']
        licId = form.cleaned_data['hiddenIdLic']
        licitacija = Licitacija.objects.get(idlicitacija=licId)
        if (iznos <= licitacija.trenutniiznos):
            errorTekst = 'Morate uneti iznos veći od trenutnog!'
        else:
            kuca = IzdavackaKuca.objects.get(username = request.user.username)
            Ponuda(iznos=iznos, idizdkuca=kuca, idlicitacija=licitacija).save()
            licitacija.trenutniiznos = iznos
            licitacija.idpobednik = izd_kuca
            licitacija.save()

    if autor or izd_kuca or request.user.is_superuser:
        if autor:
            tekuce_licitacije: Licitacija = Licitacija.objects.filter(Q(idautor=autor) & Q(datumkraja__gt=timezone.now())).order_by("datumkraja")
            protekle_licitacije: Licitacija = Licitacija.objects.filter(Q(idautor=autor) & Q(datumkraja__lt=timezone.now())).order_by("-datumkraja")
        elif izd_kuca :
            tekuce_licitacije: Licitacija = Licitacija.objects.filter(Q(datumkraja__gt=timezone.now())).order_by("datumkraja")
            protekle_licitacije: Licitacija = Licitacija.objects.filter(Q(idpobednik=izd_kuca) & Q(datumkraja__lt=timezone.now())).order_by("-datumkraja")
        elif request.user.is_superuser:
            tekuce_licitacije: Licitacija = Licitacija.objects.filter(Q(datumkraja__gt=timezone.now())).order_by("datumkraja")
            protekle_licitacije: Licitacija = Licitacija.objects.filter(Q(datumkraja__lt=timezone.now())).order_by("-datumkraja")
        return render(request, "entities/licitacije.html", {
            "pretragaForm": SearchForm(),
            "tekuce_licitacije": tekuce_licitacije,
            "protekle_licitacije": protekle_licitacije,
            "dodajLicitacijuForm": DodajLicitacijuForm(),
            'errorTekst': errorTekst,
            'licitacijaForm': LicitacijaPonudaForm()
        })
    return redirect("mojProfil")


# na osnovu zahteva koji se asinhrono salje sa klijenta
# dohvata informacije o pretrazi i vraca nazad kao odgovor
def pretragaAjax(request: HttpRequest):
    naziv = request.GET.get("naziv")
    tip = request.GET.get("tip")
    znak = ("-" if request.GET.get("filter") == "Ocena opadajuće" else "")
    objekti = []
    if tip == "Knjiga" or tip == "Sve":
        objektiz = Knjiga.objects.filter(Q(naziv__icontains=naziv) | Q(isbn__icontains=naziv)).order_by(znak + 'prosecnaocena')
        for obj in objektiz:
            objekti.append({"id": obj.isbn, "naziv": obj.naziv})
    if tip == "Korisnik" or tip == "Sve":
        objektiz = Korisnik.objects.filter((Q(imeprezime__icontains=naziv) | Q(username__icontains=naziv)) & Q(is_active=1)).order_by(znak + 'prosecnaocena')
        for obj in objektiz:
            objekti.append({"id": obj.username, "naziv": obj.imeprezime})
    if tip == "Kuća" or tip == "Sve":
        objektiz = IzdavackaKuca.objects.filter((Q(naziv__icontains=naziv) | Q(username__icontains=naziv)) & Q(is_active=1)).order_by(znak + 'prosecnaocena')
        for obj in objektiz:
            objekti.append({"id": obj.username, "naziv": obj.naziv})
    if tip == "Autor" or tip == "Sve":
        objektiz = Autor.objects.filter((Q(imeprezime__icontains=naziv) | Q(username__icontains=naziv)) & Q(is_active=1)).order_by(znak + 'prosecnaocena')
        for obj in objektiz:
            objekti.append({"id": obj.username, "naziv": obj.imeprezime})
    response = [obj.get("naziv") + " - @" + obj.get("id") for obj in objekti]
    return JsonResponse(response, safe=False)


# analogno funkciji pretragaAjax, samo sa drugacijim filterima
def pretragaAutori(request: HttpRequest):
    naziv = request.GET.get("naziv")
    objekti = []
    objektiz = Autor.objects.filter(Q(imeprezime__icontains=naziv) | Q(username__icontains=naziv))
    for obj in objektiz:
        objekti.append({"id": obj.username, "naziv": obj.imeprezime})
    response = [obj.get("naziv") + " - @" + obj.get("id") for obj in objekti]
    return JsonResponse(response, safe=False)


@login_required(login_url="login")
def dodajLicitaciju(request: HttpRequest):
    form = DodajLicitacijuForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        nazivdela = form.cleaned_data["nazivdela"]
        pdf = form.cleaned_data["pdf"]
        datumkraja = form.cleaned_data["datumkraja"]
        pocetnacena = form.cleaned_data["pocetnacena"]
        if timezone.now() > datumkraja:
            messages.error(request, 'Datum kraja nije validan')
        else:
            Licitacija(
                nazivdela=nazivdela,
                pdf=pdf,
                datumpocetka=timezone.now(),
                datumkraja=datumkraja,
                pocetnacena=pocetnacena,
                trenutniiznos=pocetnacena,
                idautor=Autor.objects.get(username=request.user.username)
            ).save()
    return redirect("licitacije")
