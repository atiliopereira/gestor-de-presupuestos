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
                        actualizar_linea(parseInt(vector[1]));
                        calcular_total();
                    }
                });
            }
        });

        $('#id_ciudad').change(function() {
            // borrar los detalles
        });

        $('#id_margen_de_ganancia').change(function() {
            actualizar_total_con_ganacia();
        });

        $('#detalledeprespuesto_set-group').click(function(e) {
            calcular_total();
         });

         $('#detalledepresupuesto_set-group').change(function(e) {

            if (e.target.id.toString().includes("cantidad")){
                row_splited =  e.target.id.split('-');
                actualizar_linea(parseInt(row_splited[1]))
            }
            calcular_total();
         });

         $('#adicionaldepresupuesto_set-group').change(function(e) {

            if (e.target.id.toString().includes("cantidad") || e.target.id.toString().includes("precio_unitario")){
                row_splited =  e.target.id.split('-');
                calcular_subtotal(parseInt(row_splited[1]))
            }
            calcular_total();
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


function calcular_total(){
    total_d = total_a = 0;
    var rows_d = $("tr[id*='detalledepresupuesto_set']");
    var rows_length_d = rows_d.length -1; // para evadir el empty

    for(var i=0 ; i<rows_length_d ; i++){
       var subtotal = document.getElementById('id_detalledepresupuesto_set-' + i + '-subtotal');
       total_d += parseInt(subtotal.value.toString().split('.').join(''));
    }

    var rows_a = $("tr[id*='adicionaldepresupuesto_set']");
    var rows_length_a = rows_a.length -1; // para evadir el empty

    for(var j=0 ; j<rows_length_a ; j++){
       var subtotal = document.getElementById('id_adicionaldepresupuesto_set-' + j + '-subtotal');
       total_a += parseInt(subtotal.value.toString().split('.').join(''));
    }

    $('#id_total').val(separarMiles(total_d + total_a));
    actualizar_total_con_ganacia();
}

function actualizar_linea(element_id){
    // Referido a los items cargados
    var cantidad = document.getElementById('id_detalledepresupuesto_set-' + element_id + '-cantidad').value;
    var precio = document.getElementById('id_detalledepresupuesto_set-' + element_id + '-precio_unitario').value;
    $("#id_detalledepresupuesto_set-" + element_id + "-subtotal").val(separarMiles(cantidad*precio));
}

function calcular_subtotal(element_id){
    // Referido a los adicionales creados por el usuario
    var cantidad = document.getElementById('id_adicionaldepresupuesto_set-' + element_id + '-cantidad').value;
    var precio = document.getElementById('id_adicionaldepresupuesto_set-' + element_id + '-precio_unitario').value;
    $("#id_adicionaldepresupuesto_set-" + element_id + "-subtotal").val(separarMiles(cantidad*precio));
}

function actualizar_total_con_ganacia(){
    var total = document.getElementById('id_total').value.toString().split('.').join('');
    var margen = parseFloat(document.getElementById('id_margen_de_ganancia').value)/100;

    $('#id_total_con_ganancia').val(separarMiles(Math.ceil(parseFloat(total) * (1 + margen))));
}


function unformat(input){
		return input.value.replace(/\./g,'').replace(',','.');
}

function separarMiles(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}