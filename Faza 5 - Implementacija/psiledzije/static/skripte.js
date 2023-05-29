//Autor: Ljubica Muravljov


// $('#myModal').on('shown.bs.modal', function () {
//     $('#myInput').trigger('focus')
//   })
//   $(function () { $('#myModal').modal({
//     keyboard: true
//  })});

$(document).ready(function () {

    $(".recenzijaEditBtn").on('click', function () {

    });

});

function resetLozinke() {
    poljeLoz = document.getElementById("promenaLozinke");
    var randomstring = Math.random().toString(36).slice(-8);
    poljeLoz.placeholder = randomstring;
}

function ukloniRec() {
    var pop = document.getElementById("novaRec")
    pop.style = "display:none;"
}

function popUp() {
    alert("Knjiga je dodata u kolekciju!");
}

function popUpPretpl() {
    alert("Pretplatili ste se na autora");
}

function dodajRec() {
    $(".modalEdit").toggle();
}


// document.getElementById("dodajRec").addEventListener("click", function() {
//
// });
function editRec(button, tekst, ocena) {

    $("#editRec").toggle();

    $("#hiddenIdRec").val(button.value);
    $("#editTeksta").val(tekst);
    $("#editOcena").val(ocena);
}

function ukloniMeni() {
    $("#dropDownRec").hide();
}

function editObjavu() {
    var pop = document.getElementById("editObj")
    pop.style = "display:block; padding:15px; "
}

function uploadEditObj() {
    var pop = document.getElementById("editObj")
    pop.style = "display:none;"
}

function showModalEdit(button, tekst, ocena) {

    $("#id_edit-tekst").val(tekst)
    $("#hiddenIdRec").val(button.value)
    $("#id_edit-ocena").val(parseInt(ocena))
    $("#editRecenzijaModal").show()

    // document.getElementById("hiddenIdRec").value =
    // document.getElementById("editTeksta").value = tekst
    // document.getElementById("editOcena").value = ocena
}

function hideModalEdit() {

}