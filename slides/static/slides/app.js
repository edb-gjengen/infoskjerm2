/* global: $, slides */
var count = 0;

$(function () {
    /* Ref: http://jquery.malsup.com/cycle/options.html */
    $("#slideshow").cycle({
        fx: "none",
        timeout: 20 * 1000,  // 20 seconds
        after: function (currSlideElement, nextSlideElement, options, forwardFlag) {
            count++;
            if (slides && slides.length) {
                currSlideElement.src = slides[count % slides.length]['url'];
            }
        }
    });

    /* Initial cycle? */
    $(".slide").each(function () {
        $("#slideshow").cycle('next');
    });
});


function updateSlides() {
    $.getJSON("/api/slides/", function (newslides) {
        slides = newslides;
    });
}
/* Initial update */
updateSlides();
/* Update slides every 2 minutes */
setInterval(updateSlides, 120 * 1000);

/* FIXME: What is this for? Hide all images after 5 seconds? */
if ($("img").length) {
    setTimeout(function () {
        $("img").hide("fast");
    }, 5 * 1000);
}

/* Every 10 minutes, reload the page */
setTimeout(function () {
    // FIXME: navigate to /
    window.location = "https://infoskjerm.neuf.no/";
}, 10 * 60 * 1000);