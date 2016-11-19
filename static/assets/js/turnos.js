$(function() {
    var turnero = $("<div>", {class:"turnero"});
    $("#div_id_hora").append(turnero);

    $("#id_fecha").on("change", function(e) {
        var dia = $(this).val();
        var promociones = $("#id_promociones").val();
        var servicios = $("#id_servicios").val();
        console.log(promociones, servicios);
        $.ajax({
            method: "GET",
            url: URL_TURNOS_LIBRES,
            data: {
                dia: dia,
                promocion: promociones,
                servicio: servicios
            },
            success: function(datos, status, req) {
                $(".turnero").empty();
                var modulos = $(datos.modulos).map(function(index, modulo) {
                    console.log(modulo);
                    var m = $("<div>", {"style": "background:" + modulo.color,
                                        "id": "div_" + index,
                                        "onclick": 'eventoHora(' + modulo.hora + ', ' + modulo.mins + ');'
                    });
                    m.html("<p>" + modulo.estado + " - " + modulo.hora + ":" + modulo.mins + "</p>");
                    return m;
                });
                modulos.each(function(i, m) {
                    turnero.append(m);
                })
            }
        })
    });
})

function eventoHora(hora, min) {
    var ret = hora + ":" + min
    $('#id_hora').val(ret)

}
