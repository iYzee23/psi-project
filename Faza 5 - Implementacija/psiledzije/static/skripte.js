//Autor: Ljubica Muravljov


// $('#myModal').on('shown.bs.modal', function () {
//     $('#myInput').trigger('focus')
//   })
//   $(function () { $('#myModal').modal({
//     keyboard: true
//  })});

// tip:
// 0-GOST 
// 1-KORISNIK 
// 2-AUTOR 
// 3-IZD KUCA 
// 4-ADMIN




function logKorisnik()
{
    document.cookie="username=1";
    document.cookie="account=0";

}
function logAutor()
{
    document.cookie="username=2";
    document.cookie="account=0";

}
function logIzdKuca()
{
    document.cookie="username=3";
    document.cookie="account=0";

}
function logAdmin()
{
    document.cookie="username=4";
    document.cookie="account=0";

}
function logOut()
{
    document.cookie="username=0";
    document.cookie="account=0";

}


function resetLozinke()
{
    poljeLoz=document.getElementById("promenaLozinke");
    var randomstring = Math.random().toString(36).slice(-8);
    poljeLoz.placeholder=randomstring;
}
function ukloniRec()
{
    var pop=document.getElementById("novaRec")
    pop.style="display:none;"
}

function inicijalizujStranicu()
{
    ulogovan=document.cookie.split("; ").find((row) => row.startsWith("username="))?.split("=")[1];
    if(ulogovan=="")
    {
        document.cookie="username=0";
        ulogovan=document.cookie;
    }

    let navmeni=document.getElementById("navmeni");
    let lista= document.createElement("ul");
    lista.classList.add("navbar-nav", "text-right");
    let desniDeo=document.getElementById("desno");
    if(ulogovan=="0")
    {
        let link=document.createElement("a");
        link.href="signup.html";
        link.classList.add("nav-link");
        link.innerText="Registruj se";
        let listel=document.createElement("li");
        listel.classList.add("nav-item");
        
        listel.appendChild(link);
        lista.appendChild(listel);

        link=document.createElement("a");
        link.href="login.html";
        link.classList.add("nav-link");
        link.innerText="Uloguj se";
        listel=document.createElement("li");
        listel.classList.add("nav-item");
        
        listel.appendChild(link);
        lista.appendChild(listel);
        desniDeo.style="padding:0px;"
        let leviDeo=document.getElementById("levi");
        // leviDeo.style="margin-left:16.666%;";
    } 
    else if(ulogovan=="4")
    {
        {
            let link=document.createElement("a");
            link.href="resetLozinke.html";
            link.classList.add("nav-link");
            link.innerText="Resetovanje lozinke";

            let listel=document.createElement("li");
            listel.classList.add("nav-item");
            
            listel.appendChild(link);
            lista.appendChild(listel);

            link=document.createElement("a");
            link.href="brisanjeNaloga.html";
            link.classList.add("nav-link");
            link.innerText="Brisanje Naloga";

            listel=document.createElement("li");
            listel.classList.add("nav-item");

            listel.appendChild(link);
            lista.appendChild(listel);

            link=document.createElement("a");
            link.href="licitacije.html";
            link.classList.add("nav-link");
            link.innerText="Licitacije";

            listel=document.createElement("li");
            listel.classList.add("nav-item");

            listel.appendChild(link);
            lista.appendChild(listel);

            // link=document.createElement("a");
            // link.href="account.html";
            // link.classList.add("nav-link");
            // link.innerText="Nalog";

            // listel=document.createElement("li");
            // listel.classList.add("nav-item");
            
            // listel.appendChild(link);
            // lista.appendChild(listel);

            link=document.createElement("a");
            link.href="index.html";
            link.classList.add("nav-link");
            link.innerText="Izloguj se";
            link.addEventListener("click", logOut);

            listel=document.createElement("li");
            listel.classList.add("nav-item");
            
            listel.appendChild(link);
            lista.appendChild(listel);
        }

        // dugme=document.createElement("input");
        // dugme.type="submit";
        // dugme.classList.add("loginbtn");
        // dugme.value="Resetovanje zaboravljene lozinke";
        
        // forma=document.createElement("form");
        // forma.action="resetLozinke.html";

        // forma.appendChild(dugme);
        
        // desniDeo.appendChild(document.createElement("br"));
        // desniDeo.appendChild(document.createElement("br"));
        // desniDeo.appendChild(forma);
        // desniDeo.appendChild(document.createElement("br"));
        // desniDeo.appendChild(document.createElement("br"));

        // dugme=document.createElement("input");
        // dugme.type="submit";
        // dugme.classList.add("loginbtn");
        // dugme.value="Brisanje korisničkog naloga";

        // forma=document.createElement("form");
        // forma.action="brisanjeNaloga.html";

        // forma.appendChild(dugme);
        // desniDeo.appendChild(forma);
        // desniDeo.appendChild(document.createElement("br"));
        // desniDeo.appendChild(document.createElement("br"));
    }
    else{
        if(ulogovan=="3")
        {
            let link=document.createElement("a");
            link.href="licitacije.html";
            link.classList.add("nav-link");
            link.innerText="Licitacije";
    
            let listel=document.createElement("li");
            listel.classList.add("nav-item");
            
            listel.appendChild(link);
            lista.appendChild(listel);
        }

        let link2=document.createElement("a");
        link2.href="account.html";
        link2.classList.add("nav-link");
        link2.innerText="Nalog";

        let listel2=document.createElement("li");
        listel2.classList.add("nav-item");
        
        listel2.appendChild(link2);
        lista.appendChild(listel2);

        link2=document.createElement("a");
        link2.href="index.html";
        link2.classList.add("nav-link");
        link2.innerText="Izloguj se";
        link2.addEventListener("click", logOut);

        listel2=document.createElement("li");
        listel2.classList.add("nav-item");
        
        listel2.appendChild(link2);
        lista.appendChild(listel2);
    }
    navmeni.appendChild(lista);
}

function inicijalizujStranicuPretraga()
{
    inicijalizujStranicu();
    levi=document.getElementById("leviDeo");
    naslov=document.createElement("h1");
    naslov.innerText="Rezultat pretrage";

    levi.appendChild(naslov);
    let linkovi=["oKnjizi.html","oAutoru.html","oKuci.html","oKorisniku.html"];
    let naslovi=["Knjiga","Autor","Izdavačka kuća","Korisnik"];
    for (var i=0;i<4;i++)
    {
        colDiv=document.createElement("div");
        colDiv.classList.add("col-sm-3");

        card=document.createElement("div");
        card.classList.add("card");

        link=document.createElement("a");
        link.href=linkovi[i];
        link.classList.add("link-secondary");

        cardImg=document.createElement("div");
        cardImg.classList.add("card-img-top");

        img=document.createElement("img");
        img.src="slike/placeholder.jpg";
        img.alt="";
        img.style="width:100%;";

        cardBody=document.createElement("div");
        cardBody.classList.add("card-body");

        title=document.createElement("h4");
        title.classList.add("card-title");
        title.innerText=naslovi[i];

        cardBody.appendChild(title);
        link.appendChild(img)
        cardImg.appendChild(link);
        card.appendChild(cardImg);
        card.appendChild(cardBody);
        colDiv.appendChild(card);
        levi.appendChild(colDiv);

    }

}

function popUp()
{
    alert("Knjiga je dodata u kolekciju!");
}

function popUpPretpl()
{
    alert("Pretplatili ste se na autora");  
}

function dodajRec()
{
    var popupDiv = document.getElementById("popupRecenzija");
    if (popupDiv.style.display == "none") {
        popupDiv.style.display = "block";
    } else {
        popupDiv.style.display = "none";
    }


}


// document.getElementById("dodajRec").addEventListener("click", function() {
//
// });
function editRec(button,tekst,ocena){
    var popupDiv = document.getElementById("editRec");
    if (popupDiv.style.display == "none") {
        popupDiv.style.display = "block";
    } else {
        popupDiv.style.display = "none";
    }
    var idRec=document.getElementById("hiddenIdRec")
    idRec.value=button.value

    var editTekst=document.getElementById("editTeksta")
    editTekst.value= tekst

    var editOcena=document.getElementById("editOcena")
    editOcena.value=ocena

}
function meniRec()
{
    var pop=document.getElementById("dropDownRec");
    pop.style="display:block; padding:15px; "
}

function ukloniMeni()
{
    var pop=document.getElementById("dropDownRec")
    pop.style="display:none;"
}

function inicijalizujStranicuOKnjizi()
{
    inicijalizujStranicu();

    let infoKnjiga=document.getElementById("infoKnjiga");
    let slikaDiv=document.createElement("div");
    slikaDiv.classList.add("col-sm-4");

    let slikaKnjige=document.createElement("img");
    slikaKnjige.classList.add("profilna");
    slikaKnjige.src=("slike/placeholder.jpg");

    slikaDiv.appendChild(slikaKnjige);
    infoKnjiga.appendChild(slikaDiv);
    let opis=document.createElement("div");
    opis.classList.add("col-sm-8")

    let naziv=document.createElement("h1");
    naziv.innerText="Naziv";
    opis.appendChild(naziv);

    let ocena=document.createElement("h3");
    ocena.innerText="4.7/5";
    ocena.style="margin-bottom:5%;";
    opis.appendChild(ocena);

    let ISBN=document.createElement("h5");
    ISBN.innerText="01011010101";
    opis.appendChild(ISBN);
    
    let autorIme=document.createElement("h5")
    autorIme.innerText="Autor Ime";
    opis.appendChild(autorIme);

    let izdKuca=document.createElement("h5")
    izdKuca.innerText="Izdavačka kuća";
    opis.appendChild(izdKuca);

    let opisKnjige=document.createElement("h5")
    opisKnjige.innerText="Opis \n Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\nAenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus \n et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, \npellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.";
    opis.appendChild(opisKnjige);

    ulogovan=document.cookie.split("; ").find((row) => row.startsWith("username="))?.split("=")[1];
    if(ulogovan!="0" && ulogovan!="3")
    { 
        let katalogDugme=document.createElement("button");
        katalogDugme.type="button";
        katalogDugme.classList.add("katalogbtn");
        katalogDugme.innerText="Dodaj u kolekciju";
        katalogDugme.onclick=popUp;
        opis.appendChild(document.createElement("br"));
        opis.appendChild(document.createElement("br"));
        opis.appendChild(katalogDugme);
    }

    infoKnjiga.appendChild(opis);
    let ispod=document.getElementById("recenzije");
    let recenzijeDiv=document.createElement("div");
    let dodajRecDiv=document.createElement("div")
    recenzijeDiv.classList.add("col-sm-10","main");
    dodajRecDiv.classList.add("col-sm-2");
    dodajRecDiv.style="padding-left:10px;";

    for(let i=0;i<2;i++)
    {
        if(ulogovan=="4")
        {
            let editBtn=document.createElement("button");
            editBtn.classList.add("editBtn");
            editBtn.innerText="...";
            editBtn.onclick=meniRec;
            recenzijeDiv.appendChild(editBtn);
        }


        let rec=document.createElement("h2");
        rec.innerText="Recenzija";

        let slika=document.createElement("img");
        slika.classList.add("fakeimg");
        
        
        recenzijeDiv.appendChild(rec);
        recenzijeDiv.appendChild(slika);

    }
    let editBtn=document.createElement("button");
    editBtn.classList.add("editBtn");
    editBtn.innerText="...";
    editBtn.onclick=meniRec;
    recenzijeDiv.appendChild(editBtn);



let rec=document.createElement("h2");
rec.innerText="Recenzija";

let slika=document.createElement("img");
slika.classList.add("fakeimg");


recenzijeDiv.appendChild(rec);
recenzijeDiv.appendChild(slika);

    ispod.appendChild(recenzijeDiv);
    if(ulogovan!="0")
    {
   
        let dodajRecBtn=document.createElement("button")
        dodajRecBtn.classList.add("katalogbtn");
        dodajRecBtn.innerText="Dodaj recenziju";
        dodajRecBtn.onclick=dodajRec
        dodajRecDiv.appendChild(dodajRecBtn)

        ispod.appendChild(dodajRecDiv)
    }
}

function inicijalizujStranicuOKorisniku()
{
    inicijalizujStranicu();

    let infoKnjiga=document.getElementById("infoKnjiga");
    let slikaDiv=document.createElement("div");
    slikaDiv.classList.add("col-sm-4");

    let slikaKnjige=document.createElement("img");
    slikaKnjige.classList.add("profilna");
    slikaKnjige.src=("slike/avatar.png");
    slikaKnjige.style="height:fit-content;"

    slikaDiv.appendChild(slikaKnjige);
    infoKnjiga.appendChild(slikaDiv);
    let opis=document.createElement("div");
    opis.classList.add("col-sm-8")

    let naziv=document.createElement("h1");
    naziv.innerText="Ime Prezime";
    opis.appendChild(naziv);

    let ocena=document.createElement("h3");
    ocena.innerText="4.5/5";
    ocena.style="margin-bottom:5%;";
    opis.appendChild(ocena);

    let Mail=document.createElement("h5");
    Mail.innerText="email@gmail.com";
    opis.appendChild(Mail);


    let biografija=document.createElement("h5")
    biografija.innerText="Biografija \n Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\nAenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus \n et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, \npellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.";
    opis.appendChild(biografija);

    ulogovan=document.cookie.split("; ").find((row) => row.startsWith("username="))?.split("=")[1];
    account=document.cookie.split("; ").find((row) => row.startsWith("account="))?.split("=")[1];


    if(ulogovan!="0")
    { 
        let katalogDugme=document.createElement("button");
        katalogDugme.type="button";
        katalogDugme.classList.add("katalogbtn");
        katalogDugme.innerText="Pretplati se";
        katalogDugme.onclick=popUpPretpl;
        if(ulogovan=="1" && account=="1")
        {
            katalogDugme.innerText="Izmeni";
            katalogDugme.onclick=function(){
                location.href="KorsnikReg.html";
            };

        }

        opis.appendChild(document.createElement("br"));
        opis.appendChild(document.createElement("br"));
        opis.appendChild(katalogDugme);
    }

    infoKnjiga.appendChild(opis);

    
    let ispod=document.getElementById("recenzije");
    let recenzijeDiv=document.createElement("div");
    let dodajRecDiv=document.createElement("div")
    recenzijeDiv.classList.add("col-sm-8","main");
    dodajRecDiv.classList.add("col-sm-4");
    dodajRecDiv.style="padding-left:10px;";

    for(let i=0;i<2;i++)
    {
        if(ulogovan=="4" || (ulogovan=="1" && account=="1"))
        {
            let editBtn=document.createElement("button");
            editBtn.classList.add("editBtn");
            editBtn.innerText="...";
            editBtn.onclick=editObjavu;
            recenzijeDiv.appendChild(editBtn);
        }


        let rec=document.createElement("h2");
        rec.innerText="Objava";

        let slika=document.createElement("img");
        slika.classList.add("fakeimg");
        
        
        recenzijeDiv.appendChild(rec);
        recenzijeDiv.appendChild(slika);

    }
    
    ispod.appendChild(recenzijeDiv);
    if(account!="1")
    {
        let recDesno=document.getElementById("recenzijeDesno");
        if(ulogovan!="0")
        {
            let dodajRecBtn=document.createElement("button")
            dodajRecBtn.classList.add("katalogbtn");
            dodajRecBtn.innerText="Dodaj recenziju";
            dodajRecBtn.onclick=dodajRec;
            dodajRecDiv.appendChild(dodajRecBtn)

            recDesno.appendChild(dodajRecDiv)
        }   
    }
}

function inicijalizujStranicuOKuci()    
{
    inicijalizujStranicu();

    let infoKnjiga=document.getElementById("infoKnjiga");
    let slikaDiv=document.createElement("div");
    slikaDiv.classList.add("col-sm-4");

    let slikaKnjige=document.createElement("img");
    slikaKnjige.classList.add("profilna");
    slikaKnjige.src=("slike/avatar.png");
    slikaKnjige.style="height:fit-content;"

    slikaDiv.appendChild(slikaKnjige);
    infoKnjiga.appendChild(slikaDiv);
    let opis=document.createElement("div");
    opis.classList.add("col-sm-8")

    let naziv=document.createElement("h1");
    naziv.innerText="Naziv";
    opis.appendChild(naziv);

    let ocena=document.createElement("h3");
    ocena.innerText="4.5/5";
    ocena.style="margin-bottom:5%;";
    opis.appendChild(ocena);

    let Mail=document.createElement("h5");
    Mail.innerText="email@gmail.com";
    opis.appendChild(Mail);

    let adresa=document.createElement("h5");
    adresa.innerText="Ulica 5";
    opis.appendChild(adresa);

    let biografija=document.createElement("h5")
    biografija.innerText="Istorija \n Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\nAenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus \n et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, \npellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.";
    opis.appendChild(biografija);

    ulogovan=document.cookie.split("; ").find((row) => row.startsWith("username="))?.split("=")[1];
    account=document.cookie.split("; ").find((row) => row.startsWith("account="))?.split("=")[1];

    if(ulogovan!="0")
    { 
        let katalogDugme=document.createElement("button");
        katalogDugme.type="button";
        katalogDugme.classList.add("katalogbtn");
        katalogDugme.innerText="Pretplati se";
        katalogDugme.onclick=popUpPretpl;

        if(ulogovan=="3" && account=="1")
        {
            katalogDugme.innerText="Izmeni";
            katalogDugme.onclick=function(){
                location.href="IzdKucaReg.html";
            }   
        }

        opis.appendChild(document.createElement("br"));
        opis.appendChild(document.createElement("br"));
        opis.appendChild(katalogDugme);
    }

    infoKnjiga.appendChild(opis);

    
    let ispod=document.getElementById("recenzije");
    let recenzijeDiv=document.createElement("div");
    let dodajRecDiv=document.createElement("div")
    recenzijeDiv.classList.add("col-sm-8","main");
    dodajRecDiv.classList.add("col-sm-4");
    dodajRecDiv.style="padding-left:10px;";

    if(ulogovan=="3" && account=="1")
    {
        let dodajObj=document.createElement("button");
        dodajObj.classList.add("katalogbtn");
        dodajObj.innerText="Dodaj Objavu";
        dodajObj.onclick=editObjavu;
        recenzijeDiv.appendChild(dodajObj);
    }

    for(let i=0;i<2;i++)
    {
        if(ulogovan=="4" || (ulogovan=="3" && account=="1"))
        {
            let editBtn=document.createElement("button");
            editBtn.classList.add("editBtn");
            editBtn.innerText="...";
            editBtn.onclick=editObjavu;
            recenzijeDiv.appendChild(editBtn);
        }


        let rec=document.createElement("h2");
        rec.innerText="Objava";

        let slika=document.createElement("img");
        slika.classList.add("fakeimg");
        
        
        recenzijeDiv.appendChild(rec);
        recenzijeDiv.appendChild(slika);

    }
    
    ispod.appendChild(recenzijeDiv);

    let recDesno=document.getElementById("recenzijeDesno");

    if(ulogovan!="0" && !(ulogovan=="3" && account=="1"))
    {
        let dodajRecBtn=document.createElement("button")
        dodajRecBtn.classList.add("katalogbtn");
        dodajRecBtn.innerText="Dodaj recenziju";
        dodajRecBtn.onclick=dodajRec;


        dodajRecDiv.appendChild(dodajRecBtn)

        recDesno.appendChild(dodajRecDiv)
    }
}

function editObjavu(){
    var pop=document.getElementById("editObj")
    pop.style="display:block; padding:15px; "
}

function uploadEditObj(){
    var pop=document.getElementById("editObj")
    pop.style="display:none;"
}

function inicijalizujStranicuOAutoru()
{
    inicijalizujStranicu();

    let infoKnjiga=document.getElementById("infoKnjiga");
    let slikaDiv=document.createElement("div");
    slikaDiv.classList.add("col-sm-4");

    let slikaKnjige=document.createElement("img");
    slikaKnjige.classList.add("profilna");
    slikaKnjige.src=("slike/avatar.png");
    slikaKnjige.style="height:fit-content;"

    slikaDiv.appendChild(slikaKnjige);
    infoKnjiga.appendChild(slikaDiv);
    let opis=document.createElement("div");
    opis.classList.add("col-sm-8")

    let naziv=document.createElement("h1");
    naziv.innerText="Ime Prezime";
    opis.appendChild(naziv);

    let ocena=document.createElement("h3");
    ocena.innerText="4.5/5";
    ocena.style="margin-bottom:5%;";
    opis.appendChild(ocena);

    let Mail=document.createElement("h5");
    Mail.innerText="email@gmail.com";
    opis.appendChild(Mail);


    let biografija=document.createElement("h5")
    biografija.innerText="Biografija \n Lorem ipsum dolor sit amet, consectetuer adipiscing elit.\nAenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus \n et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, \npellentesque eu, pretium quis, sem. Nulla consequat massa quis enim.";
    opis.appendChild(biografija);

    ulogovan=document.cookie.split("; ").find((row) => row.startsWith("username="))?.split("=")[1];
    debugger;

    account=document.cookie.split("; ").find((row) => row.startsWith("account="))?.split("=")[1];

    if(ulogovan!="0" )
    { 
        let katalogDugme=document.createElement("button");
        katalogDugme.type="button";
        katalogDugme.classList.add("katalogbtn");
        katalogDugme.innerText="Pretplati se";
        katalogDugme.onclick=popUpPretpl;

        if(ulogovan=="2" && account=="1")
        {
            // katalogDugme.classList.add("submit-button");
            katalogDugme.innerText="Izmeni sadržaj";
            katalogDugme.onclick=function(){
                location.href="AutorReg.html";
            }
        }

        opis.appendChild(document.createElement("br"));
        opis.appendChild(document.createElement("br"));
        opis.appendChild(katalogDugme);
    }

    infoKnjiga.appendChild(opis);

    
    let ispod=document.getElementById("recenzije");
    let recenzijeDiv=document.createElement("div");
    let dodajRecDiv=document.createElement("div")
    recenzijeDiv.classList.add("col-sm-8","main");
    dodajRecDiv.classList.add("col-sm-4");
    dodajRecDiv.style="padding-left:10px;";
    if(ulogovan=="2" && account=="1")
    {
        let dodajObj=document.createElement("button");
        dodajObj.classList.add("katalogbtn");
        dodajObj.innerText="Dodaj Objavu";
        dodajObj.onclick=editObjavu;
        recenzijeDiv.appendChild(dodajObj);
    }
   

    for(let i=0;i<2;i++)
    {
        debugger;
        if(ulogovan=="4" || (ulogovan=="2" && account=="1"))
        {
            let editBtn=document.createElement("button");
            editBtn.classList.add("editBtn");
            editBtn.innerText="...";
            editBtn.onclick=editObjavu;
            recenzijeDiv.appendChild(editBtn);
        }


        let rec=document.createElement("h2");
        rec.innerText="Objava";

        let slika=document.createElement("img");
        slika.classList.add("fakeimg");
        
        
        recenzijeDiv.appendChild(rec);
        recenzijeDiv.appendChild(slika);

    }
    
    ispod.appendChild(recenzijeDiv);
    if(account!="1"){
        let recDesno=document.getElementById("recenzijeDesno");
        if(ulogovan!="0" )
        {
            let dodajRecBtn=document.createElement("button")
            dodajRecBtn.classList.add("katalogbtn");
            dodajRecBtn.innerText="Dodaj recenziju";
            dodajRecBtn.style="width:fit-content; margin:0;"
            dodajRecBtn.onclick=dodajRec;
            dodajRecDiv.appendChild(dodajRecBtn)

            recDesno.appendChild(dodajRecDiv)
        }
    }
    else{
        let recDesno=document.getElementById("recenzijeDesno");

        let dodajRecBtn=document.createElement("button")
            dodajRecBtn.classList.add("katalogbtn");
            dodajRecBtn.innerText="Licitacije";
            dodajRecBtn.style="width:fit-content; margin:0;"
            dodajRecBtn.onclick=function(){
                location.href="licitacije.html";

            }
            dodajRecDiv.appendChild(dodajRecBtn)

            recDesno.appendChild(dodajRecDiv)
    }
    debugger;
    document.cookie="account=0";

}


function inicijalizujStranicuLicitaicje(){

    inicijalizujStranicu();
    levi=document.getElementById("leviDeo");
    naslov=document.createElement("h1");
    naslov.innerText="Licitacije";

    levi.appendChild(naslov);
   
    for (var i=0;i<4;i++)
    {
        colDiv=document.createElement("div");
        colDiv.classList.add("col-sm-3");

        card=document.createElement("div");
        card.classList.add("card");

        link=document.createElement("a");
        link.href="oAutoru.html";
        link.classList.add("link-secondary");

        cardImg=document.createElement("div");
        cardImg.classList.add("card-img-top");

        img=document.createElement("img");
        img.src="slike/placeholder.jpg";
        img.alt="";
        img.style="width:100%;";

        cardBody=document.createElement("div");
        cardBody.classList.add("card-body");

        title=document.createElement("h4");
        title.classList.add("card-title");
        title.innerText="Licitacija";
        cardBody.appendChild(title);
        if(ulogovan=="3")
        {
            forma=document.createElement("form");
            
            inp1=document.createElement("input");
            inp1.type="text";
            
            inp2=document.createElement("input");
            inp2.type="submit"; 
            inp2.classList.add("katalogbtn");
            inp2.value="Ponudi";

            forma.appendChild(inp1);
            forma.appendChild(inp2);
            cardBody.appendChild(forma);

        }
        link.appendChild(img)
        cardImg.appendChild(link);
        card.appendChild(cardImg);
        card.appendChild(cardBody);
        colDiv.appendChild(card);
        levi.appendChild(colDiv);

    }
   

}
function inicijalizujStranicuAccount(){
    // inicijalizujStranicu();
    document.cookie="account=1";
    ulogovan=document.cookie.split("; ").find((row) => row.startsWith("username="))?.split("=")[1];

    if(ulogovan=="1")
    {
        inicijalizujStranicuOKorisniku();
        kat=document.getElementById("katalog");
        kat.style="display:none;"
        kat=document.getElementById("kolekcija");
        kat.style="display:none;"
    }
    else if( ulogovan=="2")
    {
        inicijalizujStranicuOAutoru();
        document.cookie="account=0";
    }
    else if(ulogovan=="3")
    {

        inicijalizujStranicuOKuci();
        kat=document.getElementById("katalog");
        kat.style="display:none;"

    }
    else if(ulogovan=="4")
    {
        inicijalizujStranicuAdmin();
    }

    
    document.cookie="account=0";

}