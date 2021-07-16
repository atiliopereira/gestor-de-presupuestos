(function($) {
    jQuery(document).ready(function() {

        var rows = $("tr[id*='materialdecotizacion_set']");
        var rows_length = rows.length -1; // para evadir el empty

        if (rows_length > 0){
            document.getElementById('id_generar_items').style.visibility = 'hidden';
        } else {
            document.getElementsByClassName('field-archivo')[0].style.visibility = 'hidden';
            document.getElementsByClassName('field-comentarios')[0].style.visibility = 'hidden';
            document.getElementsByClassName('submit-row')[1].style.visibility = 'hidden';
        }
     });

})(jQuery);