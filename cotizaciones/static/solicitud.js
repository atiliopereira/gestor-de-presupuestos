(function($) {
    $(document).ready(function() {
        var tipo = document.getElementById('id_tipo');

        if(tipo.value == 'M'){
            document.getElementsByClassName('form-row field-profesionales')[0].style.display = 'none';
        } else if(tipo.value == 'S'){
            document.getElementsByClassName('form-row field-proveedores')[0].style.display = 'none';
        }
    });

})(jQuery);

