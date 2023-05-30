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