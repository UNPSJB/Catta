$(function() {
    var turnero = $("<div>", {class:"turnero"});
    $("#div_id_fecha").append(turnero);

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
    });
})

function eventoHora(hora, min, id) {
    $('.turnero').children("div").each(function() {
        $(this).css("background-color", "#5cb85c");
    });
    $('#'+id).css("background-color", '#99B898')
    console.log(id)
    var ret = hora + ":" + min
    $('#id_hora').val(ret);
}
