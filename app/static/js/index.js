$( document ).ready(function() {
  $("#view-project").click(function() {
    $('html, body').animate({
        scrollTop: $(".index").offset().top
    }, 1000);
  });
});