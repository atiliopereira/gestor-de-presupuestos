(function($) {
    $(document).ready(function() {
        var tipo = document.getElementById('id_tipo');

        if(tipo.value === 'M'){
            $('#serviciodesolicitud_set-group').hide();
        } else if(tipo.value === 'S'){
            $('#materialdesolicitud_set-group').hide();
        }
    });

})(jQuery);

