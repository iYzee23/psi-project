//Autor: Ljubica Muravljov

// $('#myModal').on('shown.bs.myModal', function () {
//     $('#myInput').trigger('focus')
//   })
//   $(function () { $('#myModal').myModal({
//     keyboard: true
//  })});
$(document).ready(function () {

    const tripleCarouselElementLicna = document.querySelector(".tripleCarousel.licna")
    const tripleCarouselElementIzdate = document.querySelector(".tripleCarousel.izdrate")
    if (window.matchMedia("(min-width: 576px)").matches) {

        const carouselLicna = new bootstrap.Carousel(tripleCarouselElementLicna,
            {
                interval: false
            })
        //licna kolekcija
        if ($(".tripleCarousel.licna .carousel-inner") && $(".tripleCarousel.licna .carousel-inner")[0]) {
            var carouselWidthLicna = $(".tripleCarousel.licna .carousel-inner")[0].scrollWidth;
            var cardWidthLicna = $(".tripleCarousel.licna .carousel-item").width();

            scrollPositionLicna = 0;

            $(".tripleCarousel.licna .carousel-control-next").on("click", function () {
                if (scrollPositionLicna < (carouselWidthLicna - cardWidthLicna * 4)) { //check if you can go any further
                    scrollPositionLicna += cardWidthLicna;  //update scroll position
                    $(".tripleCarousel.licna .carousel-inner").animate({scrollLeft: scrollPositionLicna}, 600); //scroll left
                }
            });

            $(".tripleCarousel.licna .carousel-control-prev").on("click", function () {
                if (scrollPositionLicna > 0) {
                    scrollPositionLicna -= cardWidthLicna;
                    $(".tripleCarousel.licna .carousel-inner").animate(
                        {scrollLeft: scrollPositionLicna},
                        600
                    );
                }
            });
        }
        if ($(".tripleCarousel.izdate .carousel-inner") && $(".tripleCarousel.izdate .carousel-inner")[0]) {
            //izdate knjige
            var carouselWidthIzdate = $(".tripleCarousel.izdate .carousel-inner")[0].scrollWidth;
            var cardWidthIzdate = $(".tripleCarousel.izdate .carousel-item").width();

            scrollPositionIzdate = 0;

            $(".tripleCarousel.izdate .carousel-control-next").on("click", function () {
                if (scrollPositionIzdate < (carouselWidthIzdate - cardWidthIzdate * 4)) { //check if you can go any further
                    scrollPositionIzdate += cardWidthIzdate;  //update scroll position
                    $(".tripleCarousel.izdate .carousel-inner").animate({scrollLeft: scrollPositionIzdate}, 600); //scroll left
                }
            });

            $(".tripleCarousel.izdate .carousel-control-prev").on("click", function () {
                if (scrollPositionIzdate > 0) {
                    scrollPositionIzdate -= cardWidthIzdate;
                    $(".tripleCarousel.izdate .carousel-inner").animate(
                        {scrollLeft: scrollPositionIzdate},
                        600
                    );
                }
            });
        }
    } else {
        $(tripleCarouselElementLicna).addClass("slide");
        $(tripleCarouselElementIzdate).addClass("slide");
    }


    $("#id_naziv").keyup(function () {
        $.ajax({
            url: "http://127.0.0.1:8000/pretragaAjax/",
            type: "GET",
            data: {
                naziv: $("#id_naziv").val(),
                tip: $("#id_tip").val(),
                znak: $("#id_filter").val()
            },
            success: function (response) {
                $("#id_naziv").autocomplete({
                    source: response,
                    delay: 0,
                    select: function (event, ui) {
                        var value = ui.item.value.split(" - @")[1];
                        $(this).val(value);
                        return false;
                    }
                }).data("ui-autocomplete")._renderItem = function (ul, item) {
                    var term = this.term.toLowerCase();
                    var value = item.value.split(" - @")[1];
                    var label = item.label.replace(
                        new RegExp("(" + $.ui.autocomplete.escapeRegex(term) + ")", "gi"),
                        "<b>$1</b>"
                    );
                    label = label.replace(
                        new RegExp("(" + $.ui.autocomplete.escapeRegex(value) + ")", "gi"),
                        "<b>$1</b>"
                    );
                    return $("<li></li>")
                        .data("ui-autocomplete-item", item)
                        .append("<div>" + label + "</div>")
                        .appendTo(ul);
                };
            }
        })
    });

    $("#id_novaKnjiga-autori").keyup(function() {
        $.ajax({
            url: "http://127.0.0.1:8000/pretragaAutori/",
            type: "GET",
            data: {
                naziv: $("#id_novaKnjiga-autori").val()
            },
            success: function(response) {
                $("#id_novaKnjiga-autori").autocomplete({
                    source: response,
                    delay: 0,
                    select: function(event, ui) {
                        var value = ui.item.value.split(" - @")[1];
                        $(this).val(value);
                        return false;
                    }
                }).data("ui-autocomplete")._renderItem = function(ul, item) {
                    var term = this.term.toLowerCase();
                    var value = item.value.split(" - @")[1];
                    var label = item.label.replace(
                        new RegExp("(" + $.ui.autocomplete.escapeRegex(term) + ")", "gi"),
                        "<b>$1</b>"
                    );
                    label = label.replace(
                        new RegExp("(" + $.ui.autocomplete.escapeRegex(value) + ")", "gi"),
                        "<b>$1</b>"
                    );
                    return $("<li></li>")
                        .data("ui-autocomplete-item", item)
                        .append("<div>" + label + "</div>")
                        .appendTo(ul);
                    };
            }
        })
    });

    let autori = [];

    $("#id_novaKnjiga-dodaj").on("click", function() {
        const value = $("#id_novaKnjiga-autori").val().trim();
        if (value !== '' && !autori.includes(value)) {
            $.ajax({
                url: "http://127.0.0.1:8000/pretragaAutori/",
                type: "GET",
                data: {
                    naziv: $("#id_novaKnjiga-autori").val()
                },
                success: function(response) {
                    if (JSON.stringify(response) !== "[]") {
                        autori.push(value);
                        let liItem = $('<li></li>');
                        let hidden = $('<input type="hidden" name="mojiAutori" value="' + value + '">')
                        let prikaz = $('<button type="button" class="btn btn-light dugmence"></button>');
                        let bedz = $('<span class="badge bg-danger">X</span>');
                        prikaz.text(value + " ");
                        prikaz.append(bedz);
                        liItem.append(hidden);
                        liItem.append(prikaz);
                        $('#mojiAutori').append(liItem);
                        $('#id_novaKnjiga-autori').val("");
                    }
                }
            });
        }
    });

    $('#mojiAutori').on('click', 'li .dugmence .badge', function() {
        let val = $(this).parent().text().split(" ")[0];
        let index = autori.indexOf(val);
        autori.splice(index, 1);
        $(this).closest('li').remove();
    });

    $('#dodajKnjiguForm').on("submit", function(event) {
        let ul = $("#mojiAutori");
        if (ul.children().length == 0) {
          event.preventDefault();
          alert('Morate da unesete barem jednog autora');
        }
    });

});

function showModalEdit(idRec, tekst, ocena) {
    $("#id_edit-tekst").val(tekst)
    $("#id_edit-hiddenIdRec").val(idRec)
    $("#id_edit-ocena").val(parseInt(ocena))
    $("#editRecenzijaModal").show()
}

function showModalEditFancy(idRec, tekst, ocena) {
    $("#izmeniRecenzijuForm #id_edit-tekst").val(tekst);
    $("#izmeniRecenzijuForm #id_edit-hiddenIdRec").val(idRec);
    $("#izmeniRecenzijuForm #id_edit-ocena").val(parseInt(ocena));
}

function showModalEditFancyObjava(idObjave, sadrzaj, slika) {
    $("#izmeniObjavuForm #id_objavaEdit-hiddenIdObjave").val(parseInt(idObjave));
    $("#izmeniObjavuForm #id_objavaEdit-sadrzaj").val(sadrzaj);
    $("#izmeniObjavuForm #id_objavaEdit-slika").val(slika);
    $("#izbrisiObjavuForm #id_hiddenIdObjave").val(idObjave);

}

function showModalDeleteFancyObjava(idObjave) {
    $("#izbrisiObjavuForm #id_hiddenIdObjave").val(idObjave);
}

function showModalDelete(idRec) {
    $("#hiddenIdDeleteRec").val(idRec)
    $("#deleteRecenzijaModal").show()
}

function showLicitacijaInfo(idLic) {
    $("#id_hiddenIdLic").val(idLic);
}

/*
function getCSRFToken() {
    const cookieValue = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="));

    if (cookieValue) {
        return cookieValue.split("=")[1];
    } else {
        return null;
    }
}
*/

function showModalDeleteFancy(idRec) {
    $("#hiddenIdDeleteRec").val(idRec);
}

