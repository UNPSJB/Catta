$(function() {
    var turnero = $("<div>", {class: "turnero"});
    $("#div_id_fecha").append(turnero);

    $("#id_fecha").change(function() { funcionAjax(this) });
    $("#id_empleado").change(function() { funcionAjax(this) });

    function funcionAjax(elemento) {
        var fecha = $("#id_fecha").val();
        var empleado = $("#id_empleado").val();

        if ((empleado != "")&&(fecha != "")) {
            var promociones = $("#id_promociones").val();
            var servicios = $("#id_servicios").val();
            // var empleado = $('#id_empleado').val();
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
                                            "onclick": 'eventoHora('+modulo.hora+', '+modulo.mins+', id);'
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

function eventoHora(hora, min, id) {
    $('.turnero').children("div").each(function() {
        $(this).css("background-color", "#5cb85c");
    });
    $('#'+id).css("background-color", '#99B898');
    var fecha = $('#id_fecha').val().slice(0,10);
    /* Agrega un cero adelante de la hora si es un solo digito */
    if (/^\d$/.test(hora))  {
        hora = "0" + hora;
    }
    /* Agrega un cero adelante de los minutos si es un solo digito */
    if (/^\d$/.test(min))  {
        min = "0" + min;
    }
    $('#id_fecha').val(fecha + " " + hora + ":" + min);
}
