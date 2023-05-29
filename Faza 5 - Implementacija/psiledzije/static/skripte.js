//Autor: Ljubica Muravljov

// $('#myModal').on('shown.bs.modal', function () {
//     $('#myInput').trigger('focus')
//   })
//   $(function () { $('#myModal').modal({
//     keyboard: true
//  })});
$(document).ready(function () {

});

function showModalEdit(idRec, tekst, ocena) {

    $("#id_edit-tekst").val(tekst)
    $("#id_edit-hiddenIdRec").val(idRec)
    $("#id_edit-ocena").val(parseInt(ocena))

    $("#editRecenzijaModal").show()
}
function showModalDelete(idRec) {

    $("#hiddenIdDeleteRec").val(idRec)
    $("#deleteRecenzijaModal").show()
}


function popUpPretpl()
{
    alert("Pretplatili ste se na autora");  
}

function dodajRec()
{

    $("#popupRecenzija").toggle();

    // var popupDiv = document.getElementById("popupRecenzija");
    // if (popupDiv.style.display == "none") {
    //     popupDiv.style.display = "block";
    // } else {
    //     popupDiv.style.display = "none";
    // }


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