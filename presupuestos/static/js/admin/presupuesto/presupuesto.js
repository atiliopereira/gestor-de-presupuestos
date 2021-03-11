(function($) {
    $(document).ready(function() {
        $('select').change(function(){
            vector = $(this).attr("id").split("-");
            if(vector[0] === "id_detalledepresupuesto_set"){
                var optionSelected = $(this).find("option:selected");
                var valueSelected  = optionSelected.val();
                var ciudad = document.getElementById("id_ciudad").value;
                if(!valueSelected){
                    $("#id_detalledepresupuesto_set-" + vector[1] + "-precio_unitario").val("");
                    return
                }
                $.ajax({
                    data: {"item_id": valueSelected, "ciudad_id": ciudad },
                    url: "/admin/items/getitem/",
                    type: "get",
                    success: function(data){
                        $("#id_detalledepresupuesto_set-" + vector[1] + "-precio_unitario").val(data.precio);
                        calcular_subtotal();
                    }
                });
            }
        });

        $('#id_ciudad').change(function() {

        });

        $('#detalledeprespuesto_set-group').click(function() {
            calcular_subtotal();
         });

         $('#detalledepresupuesto_set-group').change(function() {
            calcular_subtotal();
         });


        // quitar coma decimal y separadores de miles antes del submit
        $('form input[type=submit]').click(function(e) {
            $('.auto').each(function (){
                $(this).val(($(this).val()!='')?unformat(document.getElementById(this.id.toString())):'');
            });
            $('#id_total').val(parseInt(total));
        });

    });

})(jQuery);


function calcular_subtotal() {
    subtotal = 0;
    var rows = $("tr[id*='detalledepresupuesto_set']");
    var rows_length = rows.length -1; // para evadir el empty
    for( var i=0; i<rows_length; i++){
        var cantidad = document.getElementById('id_detalledepresupuesto_set-'+i+'-cantidad').value;
        var precio = document.getElementById('id_detalledepresupuesto_set-'+i+'-precio_unitario').value;
        $("#id_detalledepresupuesto_set-" + i + "-subtotal").val(separarMiles(cantidad*precio));
    }
    calcular_total();
}


function calcular_total(){
    total = 0;
    var rows = $("tr[id*='detalledepresupuesto_set']");
    var rows_length = rows.length -1; // para evadir el empty

    for(var i=0 ; i<rows_length ; i++){
       var subtotal = document.getElementById('id_detalledepresupuesto_set-'+i+'-subtotal');
       total += parseInt(subtotal.value.toString().split('.').join(''));
    }

   $('#id_total').val(separarMiles(total));
}

function unformat(input){
		return input.value.replace(/\./g,'').replace(',','.');
}

function separarMiles(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}