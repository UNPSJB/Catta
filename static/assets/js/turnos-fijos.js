$(function() {
    var turnero = $("<div>", {class: "turnero"});
    $("#div_id_fecha_fin").append(turnero);

    $("#fecha_inicio").change(function() { funcionAjax(this) });
    $("#id_empleado_fijo").change(function() { funcionAjax(this) });
    $("#id_promociones").change(function() { funcionAjax(this) });
    $("#id_servicios").change(function() { funcionAjax(this) });

    function funcionAjax(elemento) {
        var fecha = $('#fecha_inicio').val().slice(0,10);
        var empleado = $("#id_empleado_fijo").val();
        var promociones = $("#id_promociones").val();
        var servicios = $("#id_servicios").val();
        $('#fecha_inicio').val(fecha);
        console.log(fecha);
        console.log(empleado);

        if ((empleado != "")&&(fecha != "")) {
            console.log("Entre");
            $.ajax({
                method: "GET",
                url: URL_TURNOS_LIBRES,
                data: {
                    dia: fecha,
                    promocion: promociones,
                    empleado: empleado,
                    servicio: servicios
                },
                success: function(datos, status, req) {
                    $(".turnero").empty();

                    var modulos = $(datos.modulos).map(function(index, modulo) {
                        /* Agrega un cero adelante de la hora si es un solo digito */
                        if (/^\d$/.test(modulo.hora))  {
                            modulo.hora = "0" + modulo.hora
                        }
                        /* Agrega un cero adelante de los minutos si es un solo digito */
                        if (/^\d$/.test(modulo.mins))  {
                            modulo.mins = "0" + modulo.mins
                        }
                        /* Compone el div de la ventana */
                        var m = $("<div>", {"class": "turnos btn",
                                            "id": "div_" + index,
                                            "onclick": 'eventoHoraFijo('+modulo.hora+', '+modulo.mins+', id);'
                        });
                        m.html("<p>" + modulo.hora + ":" + modulo.mins + "</p>");
                        return m;
                    });
                    modulos.each(function(i, m) {
                        turnero.append(m);
                    })
                }
            })
        } else {
            $(".turnero").empty();
        }
    };

});

function eventoHoraFijo(hora, min, id) {
    $('.turnero').children("div").each(function() {
        $(this).css("background-color", "#5cb85c");
    });
    $('#'+id).css("background-color", '#99B898');
    var fecha = $('#fecha_inicio').val().slice(0,10);
    /* Agrega un cero adelante de la hora si es un solo digito */
    if (/^\d$/.test(hora))  {
        hora = "0" + hora;
    }
    /* Agrega un cero adelante de los minutos si es un solo digito */
    if (/^\d$/.test(min))  {
        min = "0" + min;
    }
    $('#fecha_inicio').val(fecha + " " + hora + ":" + min);
}
