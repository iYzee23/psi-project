//Autor: Ljubica Muravljov


// $('#myModal').on('shown.bs.modal', function () {
//     $('#myInput').trigger('focus')
//   })
//   $(function () { $('#myModal').modal({
//     keyboard: true
//  })});

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
    $("#popupRecenzija").toggle();
}


// document.getElementById("dodajRec").addEventListener("click", function() {
//
// });
function editRec(button,tekst,ocena){

    $("#editRec").toggle();

    $("#hiddenIdRec").val(button.value);
    $("#editTeksta").val(tekst);
    $("#editOcena").val(ocena);
    // var idRec=document.getElementById("hiddenIdRec");
    // idRec.value=button.value;
    //
    // var editTekst=document.getElementById("editTeksta");
    // editTekst.value= tekst;
    //
    // var editOcena=document.getElementById("editOcena");
    // editOcena.value=ocena;

}
function meniRec()
{
    var pop=document.getElementById("dropDownRec");
    pop.style="display:block; padding:15px; "
}

function ukloniMeni()
{
    $("#dropDownRec").hide();
}

function editObjavu(){
    var pop=document.getElementById("editObj")
    pop.style="display:block; padding:15px; "
}

function uploadEditObj(){
    var pop=document.getElementById("editObj")
    pop.style="display:none;"
}

function toggleModal() {
    $(".modal").toggle()
}


function showModalEdit(button, tekst, ocena) {
    $(".modalEdit").show()
    var idRec=document.getElementById("hiddenIdRec")
    idRec.value=button.value
    var editTekst=document.getElementById("editTeksta")
    editTekst.value= tekst
    var editOcena=document.getElementById("editOcena")
    editOcena.value=ocena
}

function hideModalEdit() {
    $(".modalEdit").hide()
}