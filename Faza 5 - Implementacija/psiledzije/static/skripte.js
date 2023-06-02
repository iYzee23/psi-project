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

function showModalDelete(idRec) {
    $("#hiddenIdDeleteRec").val(idRec);
    $("#deleteRecenzijaModal").show();

}
function showModalDeleteFancy(idRec) {
    $("#hiddenIdDeleteRec").val(idRec);
    console.log($("#hiddenIdDeleteRec").val())
}
