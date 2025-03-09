$( document ).ready(function() {
    $('.theme').click(function () {
        let html = $('html');
        html.attr('class', '');
        html.attr('class', $(this).val());
    });
});